# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2018.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
# Copyright 2021 Dell (www.dell.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import List, Dict, Optional, Callable, Type, Union, NamedTuple, Any
from qiskit.providers.ibmq.runtime import RuntimeProgram, RuntimeJob, ResultDecoder
from qiskit.providers.ibmq.runtime.runtime_program import ProgramParameter, ProgramResult
from qiskit.providers.ibmq.runtime.utils import RuntimeEncoder
from qiskit.providers import ProviderV1 as Provider
import hashlib
import copy
from datetime import datetime 
from pathlib import Path
import os
import json
import logging
import shutil

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from . import emulation_executor
from .emulator_runtime_job import EmulatorRuntimeJob

DIR = "DIR"
STRING = "STRING"

QDR_DIR = os.path.expanduser("~") + "/.qdr"
from .backend_provider import BackendProvider

class EmulatorRuntimeService():
    def __init__(self, provider: Provider) -> None:
        self.provider = provider
        self._programs = {}
        self._program_data = {}
        self._nextjobID = "1"
        self.backend_provider = BackendProvider()

    def backends(self) -> None:
        return self.backend_provider.backends()

    # copied from IBMQ Provider
    def pprint_programs(self, refresh: bool = False) -> None:
        """Pretty print information about available runtime programs.

        Args:
            refresh: If ``True``, re-query the server for the programs. Otherwise
                return the cached value.
        """
        programs = self.programs(refresh).values()
        for prog in programs:
            print("="*50)
            print(str(prog))

    def upload_program(
            self,
            data: Union[bytes, str],
            metadata: Optional[Union[Dict, str]] = None,
            name: Optional[str] = None,
            max_execution_time: Optional[int] = None,
            description: Optional[str] = None,
            version: Optional[float] = None,
            backend_requirements: Optional[str] = None,
            parameters: Optional[List[ProgramParameter]] = None,
            return_values: Optional[List[ProgramResult]] = None,
            interim_results: Optional[List[ProgramResult]] = None
    ) -> str:
        # careful of hash collision
        program_hash = hex(hash((data, name, version)))[-16:]
        if name is None:
            name = program_hash

        program_metadata = self._merge_metadata(
            initial={},
            metadata=metadata,
            name=name, max_execution_time=max_execution_time, description=description,
            version=version, backend_requirements=backend_requirements,
            parameters=parameters,
            return_values=return_values, interim_results=interim_results)

        program_metadata.pop('name', None)

        # data can be one of three things:
        # Filename -> read to string, send
        # Directory -> zip, send
        # String -> send

        if os.path.isdir(data):
            logger.debug(f"Have directory: {data}")
            if not os.path.isdir(QDR_DIR):
                os.mkdir(QDR_DIR)
            dirsplit = data.split("/")
            if dirsplit[-1] == "":
                if not os.path.isfile(data + "program.py"):
                    raise Exception("program.py is required for directory upload")
                if os.path.isfile(data + "executor.py") or os.path.isfile(data + "params.json"):
                    raise Exception("executor.py and params.json are unallowable names in directory")
                zipname = QDR_DIR + "/" + dirsplit[-2]
            else:
                if not os.path.isfile(data + "/program.py"):
                    raise Exception("program.py is required for directory upload")
                if os.path.isfile(data + "/executor.py") or os.path.isfile(data + "/params.json"):
                    raise Exception("executor.py and params.json are unallowable names in directory")
                zipname = QDR_DIR + "/" + dirsplit[-1]

            zipped = shutil.make_archive(zipname, "zip", data)
            logger.debug(f"made: {zipped}")
            self._program_data[program_hash] = (zipped, DIR)
        elif os.path.isfile(data):
            with open(data, "r") as f:
                self._program_data[program_hash] = (f.read(), STRING)
        else:
            logger.debug(f"Have string: {data}")
            self._program_data[program_hash] = (data, STRING)
        
        
        self._programs[program_hash] = RuntimeProgram(
            program_id = program_hash,
            creation_date= datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            program_name = name,
            **program_metadata
        )
        return program_hash

    def program(self, program_id: str, refresh: bool = False) -> RuntimeProgram:
        if program_id in self._programs:
            return self._programs[program_id]
        else:
            return None

    def programs(self, refresh: bool = False) -> List[RuntimeProgram]:
        return self._programs.copy()

    def run(
            self,
            program_id: str,
            options: Dict,
            inputs: Dict,
            callback: Optional[Callable] = None,
            result_decoder: Optional[Type[ResultDecoder]] = None
    ) -> EmulatorRuntimeJob:
        if program_id in self._programs:
            program = self._programs[program_id]
            program_data = self._program_data[program_id]

            executor = emulation_executor.EmulationExecutor(program, program_data, options, inputs)
            job = EmulatorRuntimeJob(self._nextjobID, None, executor=executor, callback = callback)
            self._nextjobID = str(int(self._nextjobID) + 1)
            return job
        else:
            return None

    def update_program(
            self,
            program_id: str,

            # We include data as a field even though we don't get it
            # back from program() as part of RuntimeProgram.
            # We are assuming it gets updated.

            data: Optional[Union[bytes, str]] = None,
            metadata: Optional[Union[Dict, str]] = None,
            name: Optional[str] = None,
            max_execution_time: Optional[int] = None,
            description: Optional[str] = None,
            version: Optional[float] = None,
            backend_requirements: Optional[str] = None,
            parameters: Optional[List[ProgramParameter]] = None,
            return_values: Optional[List[ProgramResult]] = None,
            interim_results: Optional[List[ProgramResult]] = None
    ):
        program_metadata = self._merge_metadata(
            initial={
                'name':self._programs[program_id].name, 
                'max_execution_time':self._programs[program_id].max_execution_time, 
                'description':self._programs[program_id].description,
                'version':self._programs[program_id].version, 
                'backend_requirements':self._programs[program_id].backend_requirements,
                'parameters':self._programs[program_id].parameters,
                'return_values':self._programs[program_id].return_values, 
                'interim_results':self._programs[program_id].interim_results,
            },
            metadata=metadata,
            name=name, 
            max_execution_time=max_execution_time, 
            description=description,
            version=version, 
            backend_requirements=backend_requirements,
            parameters=parameters,
            return_values=return_values, 
            interim_results=interim_results)
        program_metadata.pop('name', None)

        if data:
            if os.path.isdir(data):
                logger.debug(f"Have directory: {data}")
                if not os.path.isdir(QDR_DIR):
                    os.mkdir(QDR_DIR)
                dirsplit = data.split("/")
                if dirsplit[-1] == "":
                    if not os.path.isfile(data + "program.py"):
                        raise Exception("program.py is required for directory upload")
                    if os.path.isfile(data + "executor.py") or os.path.isfile(data + "params.json"):
                        raise Exception("executor.py and params.json are unallowable names in directory")
                    zipname = QDR_DIR + "/" + dirsplit[-2]
                else:
                    if not os.path.isfile(data + "/program.py"):
                        raise Exception("program.py is required for directory upload")
                    if os.path.isfile(data + "/executor.py") or os.path.isfile(data + "/params.json"):
                        raise Exception("executor.py and params.json are unallowable names in directory")
                    zipname = QDR_DIR + "/" + dirsplit[-1]

                zipped = shutil.make_archive(zipname, "zip", data)
                logger.debug(f"made: {zipped}")
                self._program_data[program_id] = (zipped, DIR)
            elif os.path.isfile(data):
                with open(data, "r") as f:
                    self._program_data[program_id] = (f.read(), STRING)
            elif type(data) == Union[bytes, str]:
                logger.debug(f"Have string: {data}")
                self._program_data[program_id] = (data, STRING)


        # self._program_data[program_id] = data if data else self._program_data[program_id]
        self._programs[program_id] = RuntimeProgram(
            program_id = program_id,
            creation_date= self._programs[program_id].creation_date,
            program_name = name if name else self._programs[program_id].name,
            **program_metadata
        )

        return True
        
    def delete_program(self, program_id: str) -> None:
        try:
            del self._programs[program_id]
            del self._program_data[program_id]
            return True
        except:
            return False

    def job(self, job_id: str) -> EmulatorRuntimeJob:
        print("Do nothing")

    def jobs(self, limit: int = 10, skip: int = 0) -> List[EmulatorRuntimeJob]:
        return []

    def delete_job(self, job_id: str) -> None:
        print("Do Nothing")

    def logout(self) -> None:
        print("Do Nothing")

    # copied from IBM runtime service
    def _merge_metadata(
            self,
            initial: Dict,
            metadata: Optional[Union[Dict, str]] = None,
            **kwargs: Any
    ) -> Dict:
        """Merge multiple copies of metadata.
        Args:
            initial: The initial metadata. This may be mutated.
            metadata: Name of the program metadata file or metadata dictionary.
            **kwargs: Additional metadata fields to overwrite.
        Returns:
            Merged metadata.
        """
        upd_metadata = {}
        if metadata is not None:
            if isinstance(metadata, str):
                with open(metadata, 'r') as file:
                    upd_metadata = json.load(file)
            else:
                upd_metadata = copy.deepcopy(metadata)

        self._tuple_to_dict(initial)
        initial.update(upd_metadata)


        self._tuple_to_dict(kwargs)
        for key, val in kwargs.items():
            if val is not None:
                initial[key] = val
        

        metadata_keys = ['name', 'max_execution_time', 'description', 'version',
                         'backend_requirements', 'parameters', 'return_values',
                         'interim_results']
        return {key: val for key, val in initial.items() if key in metadata_keys}

    def _tuple_to_dict(self, metadata: Dict) -> None:
        """Convert fields in metadata from named tuples to dictionaries.
        Args:
            metadata: Metadata to be converted.
        """
        for key in ['parameters', 'return_values', 'interim_results']:
            doc_list = metadata.pop(key, None)
            if not doc_list or isinstance(doc_list[0], dict):
                continue
            metadata[key] = [dict(elem._asdict()) for elem in doc_list]

    


