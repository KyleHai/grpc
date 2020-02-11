# Copyright 2020 The gRPC Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Abstract base classes for Channel objects and Multicallable objects."""

import abc
from typing import Any, AsyncIterable, Optional, Sequence

import grpc

from . import _base_call
from ._typing import (ChannelArgumentType, DeserializingFunction, MetadataType,
                      SerializingFunction)

_IMMUTABLE_EMPTY_TUPLE = tuple()


class UnaryUnaryMultiCallable(abc.ABC):
    """Factory an asynchronous unary-unary RPC stub call from client-side."""

    @abc.abstractmethod
    def __call__(self,
                 request: Any,
                 *,
                 timeout: Optional[float] = None,
                 metadata: Optional[MetadataType] = _IMMUTABLE_EMPTY_TUPLE,
                 credentials: Optional[grpc.CallCredentials] = None,
                 wait_for_ready: Optional[bool] = None,
                 compression: Optional[grpc.Compression] = None
                ) -> _base_call.UnaryUnaryCall:
        """Asynchronously invokes the underlying RPC.

        Args:
          request: The request value for the RPC.
          timeout: An optional duration of time in seconds to allow
            for the RPC.
          metadata: Optional :term:`metadata` to be transmitted to the
            service-side of the RPC.
          credentials: An optional CallCredentials for the RPC. Only valid for
            secure Channel.
          wait_for_ready: This is an EXPERIMENTAL argument. An optional
            flag to enable wait for ready mechanism
          compression: An element of grpc.compression, e.g.
            grpc.compression.Gzip. This is an EXPERIMENTAL option.

        Returns:
          A Call object instance which is an awaitable object.

        Raises:
          RpcError: Indicating that the RPC terminated with non-OK status. The
            raised RpcError will also be a Call for the RPC affording the RPC's
            metadata, status code, and details.
        """


class UnaryStreamMultiCallable(abc.ABC):
    """Affords invoking a unary-stream RPC from client-side in an asynchronous way."""

    @abc.abstractmethod
    def __call__(self,
                 request: Any,
                 *,
                 timeout: Optional[float] = None,
                 metadata: Optional[MetadataType] = _IMMUTABLE_EMPTY_TUPLE,
                 credentials: Optional[grpc.CallCredentials] = None,
                 wait_for_ready: Optional[bool] = None,
                 compression: Optional[grpc.Compression] = None
                ) -> _base_call.UnaryStreamCall:
        """Asynchronously invokes the underlying RPC.

        Args:
          request: The request value for the RPC.
          timeout: An optional duration of time in seconds to allow
            for the RPC.
          metadata: Optional :term:`metadata` to be transmitted to the
            service-side of the RPC.
          credentials: An optional CallCredentials for the RPC. Only valid for
            secure Channel.
          wait_for_ready: This is an EXPERIMENTAL argument. An optional
            flag to enable wait for ready mechanism
          compression: An element of grpc.compression, e.g.
            grpc.compression.Gzip. This is an EXPERIMENTAL option.

        Returns:
          A Call object instance which is an awaitable object.
        """


class StreamUnaryMultiCallable(abc.ABC):
    """Affords invoking a stream-unary RPC from client-side in an asynchronous way."""

    @abc.abstractmethod
    def __call__(self,
                 request_async_iterator: Optional[AsyncIterable[Any]] = None,
                 timeout: Optional[float] = None,
                 metadata: Optional[MetadataType] = _IMMUTABLE_EMPTY_TUPLE,
                 credentials: Optional[grpc.CallCredentials] = None,
                 wait_for_ready: Optional[bool] = None,
                 compression: Optional[grpc.Compression] = None
                ) -> _base_call.StreamUnaryCall:
        """Asynchronously invokes the underlying RPC.

        Args:
          request: The request value for the RPC.
          timeout: An optional duration of time in seconds to allow
            for the RPC.
          metadata: Optional :term:`metadata` to be transmitted to the
            service-side of the RPC.
          credentials: An optional CallCredentials for the RPC. Only valid for
            secure Channel.
          wait_for_ready: This is an EXPERIMENTAL argument. An optional
            flag to enable wait for ready mechanism
          compression: An element of grpc.compression, e.g.
            grpc.compression.Gzip. This is an EXPERIMENTAL option.

        Returns:
          A Call object instance which is an awaitable object.

        Raises:
          RpcError: Indicating that the RPC terminated with non-OK status. The
            raised RpcError will also be a Call for the RPC affording the RPC's
            metadata, status code, and details.
        """


class StreamStreamMultiCallable(abc.ABC):
    """Affords invoking a stream-stream RPC from client-side in an asynchronous way."""

    @abc.abstractmethod
    def __call__(self,
                 request_async_iterator: Optional[AsyncIterable[Any]] = None,
                 timeout: Optional[float] = None,
                 metadata: Optional[MetadataType] = _IMMUTABLE_EMPTY_TUPLE,
                 credentials: Optional[grpc.CallCredentials] = None,
                 wait_for_ready: Optional[bool] = None,
                 compression: Optional[grpc.Compression] = None
                ) -> _base_call.StreamStreamCall:
        """Asynchronously invokes the underlying RPC.

        Args:
          request: The request value for the RPC.
          timeout: An optional duration of time in seconds to allow
            for the RPC.
          metadata: Optional :term:`metadata` to be transmitted to the
            service-side of the RPC.
          credentials: An optional CallCredentials for the RPC. Only valid for
            secure Channel.
          wait_for_ready: This is an EXPERIMENTAL argument. An optional
            flag to enable wait for ready mechanism
          compression: An element of grpc.compression, e.g.
            grpc.compression.Gzip. This is an EXPERIMENTAL option.

        Returns:
          A Call object instance which is an awaitable object.

        Raises:
          RpcError: Indicating that the RPC terminated with non-OK status. The
            raised RpcError will also be a Call for the RPC affording the RPC's
            metadata, status code, and details.
        """


class Channel(abc.ABC):
    """Asynchronous Channel implementation.

    A cygrpc.AioChannel-backed implementation.
    """

    @abc.abstractmethod
    async def __aenter__(self):
        """Starts an asynchronous context manager.

        Returns:
          Channel the channel that was instantiated.
        """

    @abc.abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Finishes the asynchronous context manager by closing the channel.

        Still active RPCs will be cancelled.
        """

    @abc.abstractmethod
    async def close(self, grace: Optional[float] = None):
        """Closes this Channel and releases all resources held by it.

        This method immediately stops the channel from executing new RPCs in
        all cases.

        If a grace period is specified, this method wait until all active
        RPCs are finshed, once the grace period is reached the ones that haven't
        been terminated are cancelled. If a grace period is not specified
        (by passing None for grace), all existing RPCs are cancelled immediately.

        This method is idempotent.
        """

    @abc.abstractmethod
    def get_state(self,
                  try_to_connect: bool = False) -> grpc.ChannelConnectivity:
        """Check the connectivity state of a channel.

        This is an EXPERIMENTAL API.

        If the channel reaches a stable connectivity state, it is guaranteed
        that the return value of this function will eventually converge to that
        state.

        Args:
          try_to_connect: a bool indicate whether the Channel should try to
            connect to peer or not.

        Returns: A ChannelConnectivity object.
        """

    @abc.abstractmethod
    async def wait_for_state_change(
            self,
            last_observed_state: grpc.ChannelConnectivity,
    ) -> None:
        """Wait for a change in connectivity state.

        This is an EXPERIMENTAL API.

        The function blocks until there is a change in the channel connectivity
        state from the "last_observed_state". If the state is already
        different, this function will return immediately.

        There is an inherent race between the invocation of
        "Channel.wait_for_state_change" and "Channel.get_state". The state can
        change arbitrary times during the race, so there is no way to observe
        every state transition.

        If there is a need to put a timeout for this function, please refer to
        "asyncio.wait_for".

        Args:
          last_observed_state: A grpc.ChannelConnectivity object representing
            the last known state.
        """

    @abc.abstractmethod
    async def channel_ready(self) -> None:
        """Creates a coroutine that blocks until the Channel is READY."""

    @abc.abstractmethod
    def unary_unary(
            self,
            method: str,
            request_serializer: Optional[SerializingFunction] = None,
            response_deserializer: Optional[DeserializingFunction] = None
    ) -> UnaryUnaryMultiCallable:
        """Creates a UnaryUnaryMultiCallable for a unary-unary method.

        Args:
          method: The name of the RPC method.
          request_serializer: Optional behaviour for serializing the request
            message. Request goes unserialized in case None is passed.
          response_deserializer: Optional behaviour for deserializing the
            response message. Response goes undeserialized in case None
            is passed.

        Returns:
          A UnaryUnaryMultiCallable value for the named unary-unary method.
        """

    @abc.abstractmethod
    def unary_stream(
            self,
            method: str,
            request_serializer: Optional[SerializingFunction] = None,
            response_deserializer: Optional[DeserializingFunction] = None
    ) -> UnaryStreamMultiCallable:
        """Creates a UnaryStreamMultiCallable for a unary-stream method.

        Args:
          method: The name of the RPC method.
          request_serializer: Optional behaviour for serializing the request
            message. Request goes unserialized in case None is passed.
          response_deserializer: Optional behaviour for deserializing the
            response message. Response goes undeserialized in case None
            is passed.

        Returns:
          A UnarySteramMultiCallable value for the named unary-stream method.
        """

    @abc.abstractmethod
    def stream_unary(
            self,
            method: str,
            request_serializer: Optional[SerializingFunction] = None,
            response_deserializer: Optional[DeserializingFunction] = None
    ) -> StreamUnaryMultiCallable:
        """Creates a StreamUnaryMultiCallable for a stream-unary method.

        Args:
          method: The name of the RPC method.
          request_serializer: Optional behaviour for serializing the request
            message. Request goes unserialized in case None is passed.
          response_deserializer: Optional behaviour for deserializing the
            response message. Response goes undeserialized in case None
            is passed.

        Returns:
          A StreamUnaryMultiCallable value for the named stream-unary method.
        """

    @abc.abstractmethod
    def stream_stream(
            self,
            method: str,
            request_serializer: Optional[SerializingFunction] = None,
            response_deserializer: Optional[DeserializingFunction] = None
    ) -> StreamStreamMultiCallable:
        """Creates a StreamStreamMultiCallable for a stream-stream method.

        Args:
          method: The name of the RPC method.
          request_serializer: Optional behaviour for serializing the request
            message. Request goes unserialized in case None is passed.
          response_deserializer: Optional behaviour for deserializing the
            response message. Response goes undeserialized in case None
            is passed.

        Returns:
          A StreamStreamMultiCallable value for the named stream-stream method.
        """
