import idl

class ListIndexesRequest(idl.Struct):
    collection = idl.String()


# class ListIndexesResponse(idl.Struct):
#     cursor = idl.Document(
#         cid=idl.Long(),
#         ns=idl.String(),
#         firstBatch=idl.Array(idl.Document())
#     )
#     ok = idl.Bool(coerce_input=True)

if __name__ == '__main__':
    idl.gen()
