# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: degiro_connector/trading/models/trading_relay.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from degiro_connector.trading.models import trading_pb2 as degiro__connector_dot_trading_dot_models_dot_trading__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='degiro_connector/trading/models/trading_relay.proto',
  package='degiro_connector.trading_relay',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n3degiro_connector/trading/models/trading_relay.proto\x12\x1e\x64\x65giro_connector.trading_relay\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a-degiro_connector/trading/models/trading.proto\"]\n\tSetConfig\x12:\n\x0b\x63redentials\x18\x01 \x01(\x0b\x32%.degiro_connector.trading.Credentials\x12\x14\n\x0c\x61uto_connect\x18\x02 \x01(\x08\"u\n\x0c\x43onfirmOrder\x12\x35\n\x0f\x63onfirmation_id\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12.\n\x05order\x18\x02 \x01(\x0b\x32\x1f.degiro_connector.trading.Order\"\xb3\x05\n\rProductSearch\x12\x45\n\x05\x62onds\x18\x01 \x01(\x0b\x32\x34.degiro_connector.trading.ProductSearch.RequestBondsH\x00\x12\x43\n\x04\x65tfs\x18\x02 \x01(\x0b\x32\x33.degiro_connector.trading.ProductSearch.RequestETFsH\x00\x12\x45\n\x05\x66unds\x18\x03 \x01(\x0b\x32\x34.degiro_connector.trading.ProductSearch.RequestFundsH\x00\x12I\n\x07\x66utures\x18\x04 \x01(\x0b\x32\x36.degiro_connector.trading.ProductSearch.RequestFuturesH\x00\x12O\n\nleverageds\x18\x05 \x01(\x0b\x32\x39.degiro_connector.trading.ProductSearch.RequestLeveragedsH\x00\x12G\n\x06lookup\x18\x06 \x01(\x0b\x32\x35.degiro_connector.trading.ProductSearch.RequestLookupH\x00\x12I\n\x07options\x18\x07 \x01(\x0b\x32\x36.degiro_connector.trading.ProductSearch.RequestOptionsH\x00\x12G\n\x06stocks\x18\x08 \x01(\x0b\x32\x35.degiro_connector.trading.ProductSearch.RequestStocksH\x00\x12K\n\x08warrants\x18\t \x01(\x0b\x32\x37.degiro_connector.trading.ProductSearch.RequestWarrantsH\x00\x42\t\n\x07request2\xcf\x13\n\x0cTradingRelay\x12u\n\rconfirm_order\x12,.degiro_connector.trading_relay.ConfirmOrder\x1a\x34.degiro_connector.trading.Order.ConfirmationResponse\"\x00\x12j\n\x0eproduct_search\x12-.degiro_connector.trading_relay.ProductSearch\x1a\'.degiro_connector.trading.ProductSearch\"\x00\x12U\n\nset_config\x12).degiro_connector.trading_relay.SetConfig\x1a\x1a.google.protobuf.BoolValue\"\x00\x12\x62\n\x0b\x63heck_order\x12\x1f.degiro_connector.trading.Order\x1a\x30.degiro_connector.trading.Order.CheckingResponse\"\x00\x12\x41\n\x07\x63onnect\x12\x16.google.protobuf.Empty\x1a\x1c.google.protobuf.StringValue\"\x00\x12J\n\x0c\x64\x65lete_order\x12\x1c.google.protobuf.StringValue\x1a\x1a.google.protobuf.BoolValue\"\x00\x12\x45\n\x10get_account_info\x12\x16.google.protobuf.Empty\x1a\x17.google.protobuf.Struct\"\x00\x12v\n\x14get_account_overview\x12\x31.degiro_connector.trading.AccountOverview.Request\x1a).degiro_connector.trading.AccountOverview\"\x00\x12Z\n\nget_agenda\x12(.degiro_connector.trading.Agenda.Request\x1a .degiro_connector.trading.Agenda\"\x00\x12}\n\x17get_cash_account_report\x12\x33.degiro_connector.trading.CashAccountReport.Request\x1a+.degiro_connector.trading.CashAccountReport\"\x00\x12G\n\x12get_client_details\x12\x16.google.protobuf.Empty\x1a\x17.google.protobuf.Struct\"\x00\x12_\n\x13get_company_profile\x12\x1c.google.protobuf.StringValue\x1a(.degiro_connector.trading.CompanyProfile\"\x00\x12]\n\x12get_company_ratios\x12\x1c.google.protobuf.StringValue\x1a\'.degiro_connector.trading.CompanyRatios\"\x00\x12?\n\nget_config\x12\x16.google.protobuf.Empty\x1a\x17.google.protobuf.Struct\"\x00\x12U\n\x13get_favourites_list\x12\x16.google.protobuf.Empty\x1a$.degiro_connector.trading.Favourites\"\x00\x12i\n\x18get_financial_statements\x12\x1c.google.protobuf.StringValue\x1a-.degiro_connector.trading.FinancialStatements\"\x00\x12g\n\x0fget_latest_news\x12,.degiro_connector.trading.LatestNews.Request\x1a$.degiro_connector.trading.LatestNews\"\x00\x12q\n\x13get_news_by_company\x12/.degiro_connector.trading.NewsByCompany.Request\x1a\'.degiro_connector.trading.NewsByCompany\"\x00\x12p\n\x12get_orders_history\x12/.degiro_connector.trading.OrdersHistory.Request\x1a\'.degiro_connector.trading.OrdersHistory\"\x00\x12_\n\x13get_products_config\x12\x16.google.protobuf.Empty\x1a..degiro_connector.trading.ProductSearch.Config\"\x00\x12m\n\x11get_products_info\x12..degiro_connector.trading.ProductsInfo.Request\x1a&.degiro_connector.trading.ProductsInfo\"\x00\x12Z\n\x14get_top_news_preview\x12\x16.google.protobuf.Empty\x1a(.degiro_connector.trading.TopNewsPreview\"\x00\x12\x82\x01\n\x18get_transactions_history\x12\x35.degiro_connector.trading.TransactionsHistory.Request\x1a-.degiro_connector.trading.TransactionsHistory\"\x00\x12^\n\nget_update\x12,.degiro_connector.trading.Update.RequestList\x1a .degiro_connector.trading.Update\"\x00\x12>\n\x06logout\x12\x16.google.protobuf.Empty\x1a\x1a.google.protobuf.BoolValue\"\x00\x12M\n\x0cupdate_order\x12\x1f.degiro_connector.trading.Order\x1a\x1a.google.protobuf.BoolValue\"\x00\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,degiro__connector_dot_trading_dot_models_dot_trading__pb2.DESCRIPTOR,])




_SETCONFIG = _descriptor.Descriptor(
  name='SetConfig',
  full_name='degiro_connector.trading_relay.SetConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='credentials', full_name='degiro_connector.trading_relay.SetConfig.credentials', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='auto_connect', full_name='degiro_connector.trading_relay.SetConfig.auto_connect', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=225,
  serialized_end=318,
)


_CONFIRMORDER = _descriptor.Descriptor(
  name='ConfirmOrder',
  full_name='degiro_connector.trading_relay.ConfirmOrder',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='confirmation_id', full_name='degiro_connector.trading_relay.ConfirmOrder.confirmation_id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='order', full_name='degiro_connector.trading_relay.ConfirmOrder.order', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=320,
  serialized_end=437,
)


_PRODUCTSEARCH = _descriptor.Descriptor(
  name='ProductSearch',
  full_name='degiro_connector.trading_relay.ProductSearch',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='bonds', full_name='degiro_connector.trading_relay.ProductSearch.bonds', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='etfs', full_name='degiro_connector.trading_relay.ProductSearch.etfs', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='funds', full_name='degiro_connector.trading_relay.ProductSearch.funds', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='futures', full_name='degiro_connector.trading_relay.ProductSearch.futures', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='leverageds', full_name='degiro_connector.trading_relay.ProductSearch.leverageds', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lookup', full_name='degiro_connector.trading_relay.ProductSearch.lookup', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='options', full_name='degiro_connector.trading_relay.ProductSearch.options', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stocks', full_name='degiro_connector.trading_relay.ProductSearch.stocks', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='warrants', full_name='degiro_connector.trading_relay.ProductSearch.warrants', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
    _descriptor.OneofDescriptor(
      name='request', full_name='degiro_connector.trading_relay.ProductSearch.request',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=440,
  serialized_end=1131,
)

_SETCONFIG.fields_by_name['credentials'].message_type = degiro__connector_dot_trading_dot_models_dot_trading__pb2._CREDENTIALS
_CONFIRMORDER.fields_by_name['confirmation_id'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CONFIRMORDER.fields_by_name['order'].message_type = degiro__connector_dot_trading_dot_models_dot_trading__pb2._ORDER
_PRODUCTSEARCH.fields_by_name['bonds'].message_type = degiro__connector_dot_trading_dot_models_dot_trading__pb2._PRODUCTSEARCH_REQUESTBONDS
_PRODUCTSEARCH.fields_by_name['etfs'].message_type = degiro__connector_dot_trading_dot_models_dot_trading__pb2._PRODUCTSEARCH_REQUESTETFS
_PRODUCTSEARCH.fields_by_name['funds'].message_type = degiro__connector_dot_trading_dot_models_dot_trading__pb2._PRODUCTSEARCH_REQUESTFUNDS
_PRODUCTSEARCH.fields_by_name['futures'].message_type = degiro__connector_dot_trading_dot_models_dot_trading__pb2._PRODUCTSEARCH_REQUESTFUTURES
_PRODUCTSEARCH.fields_by_name['leverageds'].message_type = degiro__connector_dot_trading_dot_models_dot_trading__pb2._PRODUCTSEARCH_REQUESTLEVERAGEDS
_PRODUCTSEARCH.fields_by_name['lookup'].message_type = degiro__connector_dot_trading_dot_models_dot_trading__pb2._PRODUCTSEARCH_REQUESTLOOKUP
_PRODUCTSEARCH.fields_by_name['options'].message_type = degiro__connector_dot_trading_dot_models_dot_trading__pb2._PRODUCTSEARCH_REQUESTOPTIONS
_PRODUCTSEARCH.fields_by_name['stocks'].message_type = degiro__connector_dot_trading_dot_models_dot_trading__pb2._PRODUCTSEARCH_REQUESTSTOCKS
_PRODUCTSEARCH.fields_by_name['warrants'].message_type = degiro__connector_dot_trading_dot_models_dot_trading__pb2._PRODUCTSEARCH_REQUESTWARRANTS
_PRODUCTSEARCH.oneofs_by_name['request'].fields.append(
  _PRODUCTSEARCH.fields_by_name['bonds'])
_PRODUCTSEARCH.fields_by_name['bonds'].containing_oneof = _PRODUCTSEARCH.oneofs_by_name['request']
_PRODUCTSEARCH.oneofs_by_name['request'].fields.append(
  _PRODUCTSEARCH.fields_by_name['etfs'])
_PRODUCTSEARCH.fields_by_name['etfs'].containing_oneof = _PRODUCTSEARCH.oneofs_by_name['request']
_PRODUCTSEARCH.oneofs_by_name['request'].fields.append(
  _PRODUCTSEARCH.fields_by_name['funds'])
_PRODUCTSEARCH.fields_by_name['funds'].containing_oneof = _PRODUCTSEARCH.oneofs_by_name['request']
_PRODUCTSEARCH.oneofs_by_name['request'].fields.append(
  _PRODUCTSEARCH.fields_by_name['futures'])
_PRODUCTSEARCH.fields_by_name['futures'].containing_oneof = _PRODUCTSEARCH.oneofs_by_name['request']
_PRODUCTSEARCH.oneofs_by_name['request'].fields.append(
  _PRODUCTSEARCH.fields_by_name['leverageds'])
_PRODUCTSEARCH.fields_by_name['leverageds'].containing_oneof = _PRODUCTSEARCH.oneofs_by_name['request']
_PRODUCTSEARCH.oneofs_by_name['request'].fields.append(
  _PRODUCTSEARCH.fields_by_name['lookup'])
_PRODUCTSEARCH.fields_by_name['lookup'].containing_oneof = _PRODUCTSEARCH.oneofs_by_name['request']
_PRODUCTSEARCH.oneofs_by_name['request'].fields.append(
  _PRODUCTSEARCH.fields_by_name['options'])
_PRODUCTSEARCH.fields_by_name['options'].containing_oneof = _PRODUCTSEARCH.oneofs_by_name['request']
_PRODUCTSEARCH.oneofs_by_name['request'].fields.append(
  _PRODUCTSEARCH.fields_by_name['stocks'])
_PRODUCTSEARCH.fields_by_name['stocks'].containing_oneof = _PRODUCTSEARCH.oneofs_by_name['request']
_PRODUCTSEARCH.oneofs_by_name['request'].fields.append(
  _PRODUCTSEARCH.fields_by_name['warrants'])
_PRODUCTSEARCH.fields_by_name['warrants'].containing_oneof = _PRODUCTSEARCH.oneofs_by_name['request']
DESCRIPTOR.message_types_by_name['SetConfig'] = _SETCONFIG
DESCRIPTOR.message_types_by_name['ConfirmOrder'] = _CONFIRMORDER
DESCRIPTOR.message_types_by_name['ProductSearch'] = _PRODUCTSEARCH
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SetConfig = _reflection.GeneratedProtocolMessageType('SetConfig', (_message.Message,), {
  'DESCRIPTOR' : _SETCONFIG,
  '__module__' : 'degiro_connector.trading.models.trading_relay_pb2'
  # @@protoc_insertion_point(class_scope:degiro_connector.trading_relay.SetConfig)
  })
_sym_db.RegisterMessage(SetConfig)

ConfirmOrder = _reflection.GeneratedProtocolMessageType('ConfirmOrder', (_message.Message,), {
  'DESCRIPTOR' : _CONFIRMORDER,
  '__module__' : 'degiro_connector.trading.models.trading_relay_pb2'
  # @@protoc_insertion_point(class_scope:degiro_connector.trading_relay.ConfirmOrder)
  })
_sym_db.RegisterMessage(ConfirmOrder)

ProductSearch = _reflection.GeneratedProtocolMessageType('ProductSearch', (_message.Message,), {
  'DESCRIPTOR' : _PRODUCTSEARCH,
  '__module__' : 'degiro_connector.trading.models.trading_relay_pb2'
  # @@protoc_insertion_point(class_scope:degiro_connector.trading_relay.ProductSearch)
  })
_sym_db.RegisterMessage(ProductSearch)



_TRADINGRELAY = _descriptor.ServiceDescriptor(
  name='TradingRelay',
  full_name='degiro_connector.trading_relay.TradingRelay',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1134,
  serialized_end=3645,
  methods=[
  _descriptor.MethodDescriptor(
    name='confirm_order',
    full_name='degiro_connector.trading_relay.TradingRelay.confirm_order',
    index=0,
    containing_service=None,
    input_type=_CONFIRMORDER,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._ORDER_CONFIRMATIONRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='product_search',
    full_name='degiro_connector.trading_relay.TradingRelay.product_search',
    index=1,
    containing_service=None,
    input_type=_PRODUCTSEARCH,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._PRODUCTSEARCH,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='set_config',
    full_name='degiro_connector.trading_relay.TradingRelay.set_config',
    index=2,
    containing_service=None,
    input_type=_SETCONFIG,
    output_type=google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='check_order',
    full_name='degiro_connector.trading_relay.TradingRelay.check_order',
    index=3,
    containing_service=None,
    input_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._ORDER,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._ORDER_CHECKINGRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='connect',
    full_name='degiro_connector.trading_relay.TradingRelay.connect',
    index=4,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='delete_order',
    full_name='degiro_connector.trading_relay.TradingRelay.delete_order',
    index=5,
    containing_service=None,
    input_type=google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE,
    output_type=google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_account_info',
    full_name='degiro_connector.trading_relay.TradingRelay.get_account_info',
    index=6,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=google_dot_protobuf_dot_struct__pb2._STRUCT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_account_overview',
    full_name='degiro_connector.trading_relay.TradingRelay.get_account_overview',
    index=7,
    containing_service=None,
    input_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._ACCOUNTOVERVIEW_REQUEST,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._ACCOUNTOVERVIEW,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_agenda',
    full_name='degiro_connector.trading_relay.TradingRelay.get_agenda',
    index=8,
    containing_service=None,
    input_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._AGENDA_REQUEST,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._AGENDA,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_cash_account_report',
    full_name='degiro_connector.trading_relay.TradingRelay.get_cash_account_report',
    index=9,
    containing_service=None,
    input_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._CASHACCOUNTREPORT_REQUEST,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._CASHACCOUNTREPORT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_client_details',
    full_name='degiro_connector.trading_relay.TradingRelay.get_client_details',
    index=10,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=google_dot_protobuf_dot_struct__pb2._STRUCT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_company_profile',
    full_name='degiro_connector.trading_relay.TradingRelay.get_company_profile',
    index=11,
    containing_service=None,
    input_type=google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._COMPANYPROFILE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_company_ratios',
    full_name='degiro_connector.trading_relay.TradingRelay.get_company_ratios',
    index=12,
    containing_service=None,
    input_type=google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._COMPANYRATIOS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_config',
    full_name='degiro_connector.trading_relay.TradingRelay.get_config',
    index=13,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=google_dot_protobuf_dot_struct__pb2._STRUCT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_favourites_list',
    full_name='degiro_connector.trading_relay.TradingRelay.get_favourites_list',
    index=14,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._FAVOURITES,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_financial_statements',
    full_name='degiro_connector.trading_relay.TradingRelay.get_financial_statements',
    index=15,
    containing_service=None,
    input_type=google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._FINANCIALSTATEMENTS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_latest_news',
    full_name='degiro_connector.trading_relay.TradingRelay.get_latest_news',
    index=16,
    containing_service=None,
    input_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._LATESTNEWS_REQUEST,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._LATESTNEWS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_news_by_company',
    full_name='degiro_connector.trading_relay.TradingRelay.get_news_by_company',
    index=17,
    containing_service=None,
    input_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._NEWSBYCOMPANY_REQUEST,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._NEWSBYCOMPANY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_orders_history',
    full_name='degiro_connector.trading_relay.TradingRelay.get_orders_history',
    index=18,
    containing_service=None,
    input_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._ORDERSHISTORY_REQUEST,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._ORDERSHISTORY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_products_config',
    full_name='degiro_connector.trading_relay.TradingRelay.get_products_config',
    index=19,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._PRODUCTSEARCH_CONFIG,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_products_info',
    full_name='degiro_connector.trading_relay.TradingRelay.get_products_info',
    index=20,
    containing_service=None,
    input_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._PRODUCTSINFO_REQUEST,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._PRODUCTSINFO,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_top_news_preview',
    full_name='degiro_connector.trading_relay.TradingRelay.get_top_news_preview',
    index=21,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._TOPNEWSPREVIEW,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_transactions_history',
    full_name='degiro_connector.trading_relay.TradingRelay.get_transactions_history',
    index=22,
    containing_service=None,
    input_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._TRANSACTIONSHISTORY_REQUEST,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._TRANSACTIONSHISTORY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_update',
    full_name='degiro_connector.trading_relay.TradingRelay.get_update',
    index=23,
    containing_service=None,
    input_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._UPDATE_REQUESTLIST,
    output_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._UPDATE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='logout',
    full_name='degiro_connector.trading_relay.TradingRelay.logout',
    index=24,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='update_order',
    full_name='degiro_connector.trading_relay.TradingRelay.update_order',
    index=25,
    containing_service=None,
    input_type=degiro__connector_dot_trading_dot_models_dot_trading__pb2._ORDER,
    output_type=google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TRADINGRELAY)

DESCRIPTOR.services_by_name['TradingRelay'] = _TRADINGRELAY

# @@protoc_insertion_point(module_scope)
