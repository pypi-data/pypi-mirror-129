# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/protobuf/status.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorflow/core/protobuf/status.proto',
  package='tensorflow',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n%tensorflow/core/protobuf/status.proto\x12\ntensorflow\"\x0f\n\rDerivedStatusb\x06proto3'
)




_DERIVEDSTATUS = _descriptor.Descriptor(
  name='DerivedStatus',
  full_name='tensorflow.DerivedStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=53,
  serialized_end=68,
)

DESCRIPTOR.message_types_by_name['DerivedStatus'] = _DERIVEDSTATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DerivedStatus = _reflection.GeneratedProtocolMessageType('DerivedStatus', (_message.Message,), {
  'DESCRIPTOR' : _DERIVEDSTATUS,
  '__module__' : 'tensorflow.core.protobuf.status_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.DerivedStatus)
  })
_sym_db.RegisterMessage(DerivedStatus)


# @@protoc_insertion_point(module_scope)
