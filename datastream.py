from pyfca import Pyfca, DropChunk
import asyncio
from ansi_color_codes import *
from os import environ
import utils
from collections.abc import Iterable

DEBUG = 'DATASTREAM_DEBUG' in environ or 'SCRAMJET_DEBUG' in environ
tr = utils.print_trimmed

def log(stream, *args):
    if DEBUG:
        utils.LogWithTimer.log(f"{grey}{stream.name}{reset}", *args)


class UnsupportedOperation(Exception):
    pass


class DataStream():
    def __init__(self, max_parallel=64, upstream=None, name="datastream"):
        self.upstream = upstream
        self.name = name
        self.pyfca = upstream.pyfca if upstream else Pyfca(max_parallel)
        self.ready_to_start = asyncio.Future()
        log(self, f'INIT stream created with pyfca {self.pyfca}')

    def _uncork(self):
        self.ready_to_start.set_result(True)
        log(self, f'{green}uncorked{reset}')
        if self.upstream:
            log(self, f'uncorking upstream: {self.upstream.name}')
            self.upstream._uncork()

    @staticmethod
    def read_from(source, max_parallel=64, chunk_size=None):
        if chunk_size:
            if hasattr(source, 'read'):
                return DataStream.from_reader(source, chunk_size=chunk_size)
        elif isinstance(source, Iterable):
            return DataStream.from_iterable(source)

        raise UnsupportedOperation

    @staticmethod
    def from_iterable(iterable, max_parallel=64):
        stream = DataStream(max_parallel)
        async def consume():
            await stream.ready_to_start
            for item in iterable:
                await stream.pyfca.write(item)
            stream.pyfca.end()

        asyncio.create_task(consume())
        return stream

    @staticmethod
    def from_reader(reader, max_parallel=64, chunk_size=4096):
        stream = DataStream(max_parallel)

        async def consume():
            await stream.ready_to_start
            while True:
                chunk = reader.read(chunk_size)
                if chunk == '' or chunk == b'':
                    break
                await stream.pyfca.write(chunk)
            stream.pyfca.end()

        asyncio.create_task(consume())
        return stream

    def flatmap(self, func, *args):
        new_stream = DataStream(max_parallel=self.pyfca.max_parallel, name=f'{self.name}+fm')
        async def consume():
            self._uncork()
            while True:
                chunk = await self.pyfca.read()
                log(self, f'got: {tr(chunk)}')
                if chunk is None:
                    break
                results = func(chunk, *args)
                if asyncio.iscoroutine(results):
                    results = await results
                log(self, f'{cyan}split:{reset} -> {repr(results)}')
                for item in results:
                    log(new_stream, f'put: {tr(item)}')
                    await new_stream.pyfca.write(item)
                    log(new_stream, f'{blue}drained{reset}')
            log(new_stream, f'ending pyfca {new_stream.pyfca}')
            new_stream.pyfca.end()
        asyncio.create_task(consume(), name='flatmap-consumer')
        return new_stream

    def filter(self, func, *args):
        new_stream = DataStream(upstream=self, name=f'{self.name}+f')
        async def run_filter(chunk):
            if args:
                log(new_stream, f'calling filter {func} with args: {chunk, *args}')
            decision = func(chunk, *args)
            if asyncio.iscoroutine(decision):
                decision = await decision
            log(new_stream, f'filter result: {tr(chunk)} -> {cyan}{decision}{reset}')
            return chunk if decision else DropChunk
        log(new_stream, f'adding filter: {func}')
        new_stream.pyfca.add_transform(run_filter)
        return new_stream

    def sequence(self, sequencer, initialPartial=None):
        new_stream = DataStream(max_parallel=self.pyfca.max_parallel, name=f'{self.name}+s')
        async def consume():
            self._uncork()
            partial = initialPartial

            while True:
                chunk = await self.pyfca.read()
                log(self, f'got: {tr(chunk)}')
                if chunk is None:
                    break
                chunks = sequencer(partial, chunk)
                if asyncio.iscoroutine(chunks):
                    chunks = await chunks
                log(new_stream, f'{blue}{len(chunks)} chunks:{reset} {chunks}')
                for chunk in chunks[:-1]:
                    log(new_stream, f'put: {tr(chunk)}')
                    await new_stream.pyfca.write(chunk)
                log(new_stream, f'carrying over partial result: {tr(chunks[-1])}')
                partial = chunks[-1]

            log(new_stream, f'leftover: {tr(partial)}')
            if partial:
                log(new_stream, f'put: {tr(partial)}')
                await new_stream.pyfca.write(partial)
            log(new_stream, f'ending pyfca {new_stream.pyfca}')
            new_stream.pyfca.end()
        asyncio.create_task(consume())
        return new_stream

    def map(self, func, *args):
        new_stream = DataStream(upstream=self, name=f'{self.name}+m')
        async def run_mapper(chunk):
            if args:
                log(new_stream, f'calling mapper {func} with args: {chunk, *args}')
            result = func(chunk, *args)
            if asyncio.iscoroutine(result):
                result = await result
            log(new_stream, f'mapper result: {tr(chunk)} -> {tr(result)}')
            return result
        log(new_stream, f'adding mapper: {func}')
        new_stream.pyfca.add_transform(run_mapper)
        return new_stream

    def batch(self, func, *args):
        new_stream = DataStream(max_parallel=self.pyfca.max_parallel, name=f'{self.name}+b')
        async def consume():
            self._uncork()
            batch = []

            while True:
                chunk = await self.pyfca.read()
                log(self, f'got: {tr(chunk)}')
                if chunk is None:
                    break
                batch.append(chunk)
                if args:
                    log(new_stream, f'calling {func} with args: {chunk, *args}')
                if func(chunk, *args):
                    log(new_stream, f'{pink}put batch:{reset} {tr(batch)}')
                    await new_stream.pyfca.write(batch)
                    batch = []

            if len(batch):
                log(new_stream, f'{pink}put batch:{reset} {tr(batch)}')
                await new_stream.pyfca.write(batch)

            log(new_stream, f'ending pyfca {new_stream.pyfca}')
            new_stream.pyfca.end()
        asyncio.create_task(consume())
        return new_stream

    async def to_list(self):
        self._uncork()
        result = []
        log(self, f'sink: {repr(result)}')
        chunk = await self.pyfca.read()
        while chunk is not None:
            log(self, f'got: {tr(chunk)}')
            result.append(chunk)
            chunk = await self.pyfca.read()
        return result

    async def to_file(self, out_file):
        self._uncork()
        log(self, f'sink: {repr(out_file)}')
        with open(out_file, 'wb') as f:
            log(self, f'writing to {f}')
            chunk = await self.pyfca.read()
            while chunk is not None:
                log(self, f'got: {tr(chunk)}')
                f.write(chunk)
                chunk = await self.pyfca.read()

    async def reduce(self, func, initial=None):
        self._uncork()
        if initial is None:
            accumulator = await self.pyfca.read()
            log(self, f'got: {tr(accumulator)}')
        else:
            accumulator = initial
            log(self, f'reducer: initialized accumulator with {initial}')
        while True:
            chunk = await self.pyfca.read()
            log(self, f'got: {tr(chunk)}')
            if chunk is None:
                break
            accumulator = func(accumulator, chunk)
            if asyncio.iscoroutine(accumulator):
                accumulator = await accumulator
            log(self, f'reduce - intermediate result: {accumulator}')
        return accumulator
