class RPCError(Exception): ...


class RPCUnknownJobStatusError(RPCError): ...


class RPCFailedJobError(RPCError): ...
