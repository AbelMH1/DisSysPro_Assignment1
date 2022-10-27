# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import wordgame_pb2 as wordgame__pb2


class WordGameStub(object):
    """The WordGame service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.FirstConnection = channel.unary_unary(
                '/protos.WordGame/FirstConnection',
                request_serializer=wordgame__pb2.WelcomeRequest.SerializeToString,
                response_deserializer=wordgame__pb2.WelcomeReply.FromString,
                )
        self.SelectMode = channel.unary_unary(
                '/protos.WordGame/SelectMode',
                request_serializer=wordgame__pb2.ModeRequest.SerializeToString,
                response_deserializer=wordgame__pb2.ModeReply.FromString,
                )
        self.GuessLetter = channel.unary_unary(
                '/protos.WordGame/GuessLetter',
                request_serializer=wordgame__pb2.LetterRequest.SerializeToString,
                response_deserializer=wordgame__pb2.LetterReply.FromString,
                )


class WordGameServicer(object):
    """The WordGame service definition.
    """

    def FirstConnection(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SelectMode(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GuessLetter(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WordGameServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'FirstConnection': grpc.unary_unary_rpc_method_handler(
                    servicer.FirstConnection,
                    request_deserializer=wordgame__pb2.WelcomeRequest.FromString,
                    response_serializer=wordgame__pb2.WelcomeReply.SerializeToString,
            ),
            'SelectMode': grpc.unary_unary_rpc_method_handler(
                    servicer.SelectMode,
                    request_deserializer=wordgame__pb2.ModeRequest.FromString,
                    response_serializer=wordgame__pb2.ModeReply.SerializeToString,
            ),
            'GuessLetter': grpc.unary_unary_rpc_method_handler(
                    servicer.GuessLetter,
                    request_deserializer=wordgame__pb2.LetterRequest.FromString,
                    response_serializer=wordgame__pb2.LetterReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'protos.WordGame', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WordGame(object):
    """The WordGame service definition.
    """

    @staticmethod
    def FirstConnection(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/protos.WordGame/FirstConnection',
            wordgame__pb2.WelcomeRequest.SerializeToString,
            wordgame__pb2.WelcomeReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SelectMode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/protos.WordGame/SelectMode',
            wordgame__pb2.ModeRequest.SerializeToString,
            wordgame__pb2.ModeReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GuessLetter(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/protos.WordGame/GuessLetter',
            wordgame__pb2.LetterRequest.SerializeToString,
            wordgame__pb2.LetterReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
