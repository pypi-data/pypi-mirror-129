# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# pyre-unsafe

from typing import Any, SupportsBytes, Union

def force_text(
    s: Any, encoding: str = ..., strings_only: bool = ..., errors: str = ...
) -> str: ...
def force_str(
    s: Union[str, bytes],
    encoding: str = ...,
    strings_only: bool = ...,
    errors: str = ...,
) -> str: ...
def force_bytes(
    s: Union[str, SupportsBytes],
    encoding: str = ...,
    strings_only: bool = ...,
    errors: str = ...,
) -> bytes: ...
def smart_text(
    s: str, encoding: str = ..., strings_only: bool = ..., errors: str = ...
) -> Any: ...
def smart_str(
    s: object, encoding: str = ..., strings_only: bool = ..., errors: str = ...
) -> Any: ...
def smart_bytes(
    s: bytes, encoding: str = ..., strings_only: bool = ..., errors: str = ...
) -> Any: ...
def iri_to_uri(iri: str) -> str: ...
