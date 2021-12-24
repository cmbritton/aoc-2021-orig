from bitarray import bitarray
from enum import Enum
import sys


class Packet(object):
    class Type(Enum):
        SUM = 0
        PRODUCT = 1
        MIN = 2
        MAX = 3
        LITERAL = 4
        GREATER_THAN = 5
        LESS_THAN = 6
        EQUAL_TO = 7

    VERSION_OFFSET = 0
    VERSION_LENGTH = 3
    TYPE_OFFSET = 3
    TYPE_LENGTH = 3
    HEADER_LENGTH = TYPE_OFFSET + TYPE_LENGTH

    def __init__(self, packet_bits):
        self.packet_bits = packet_bits

    def version(self):
        return Packet._version(self.packet_bits)

    @staticmethod
    def _version(packet_bits):
        return int(packet_bits[Packet.VERSION_OFFSET:Packet.VERSION_OFFSET + Packet.VERSION_LENGTH].to01(), 2)

    def p_type(self):
        return Packet._p_type(self.packet_bits)

    @staticmethod
    def _p_type(packet_bits):
        return int(packet_bits[Packet.TYPE_OFFSET:Packet.TYPE_OFFSET + Packet.TYPE_LENGTH].to01(), 2)

    def is_operator(self):
        return not self.is_literal()

    def is_sum(self):
        return Packet._is_sum(self.packet_bits)

    @staticmethod
    def _is_sum(packet_bits):
        return bool(Packet._p_type(packet_bits) == Packet.Type.SUM.value)

    def is_product(self):
        return Packet._is_product(self.packet_bits)

    @staticmethod
    def _is_product(packet_bits):
        return bool(Packet._p_type(packet_bits) == Packet.Type.PRODUCT.value)

    def is_min(self):
        return Packet._is_min(self.packet_bits)

    @staticmethod
    def _is_min(packet_bits):
        return bool(Packet._p_type(packet_bits) == Packet.Type.MIN.value)

    def is_max(self):
        return Packet._is_max(self.packet_bits)

    @staticmethod
    def _is_max(packet_bits):
        return bool(Packet._p_type(packet_bits) == Packet.Type.MAX.value)

    def is_literal(self):
        return Packet._is_literal(self.packet_bits)

    @staticmethod
    def _is_literal(packet_bits):
        return bool(Packet._p_type(packet_bits) == Packet.Type.LITERAL.value)

    def is_greater_than(self):
        return Packet._is_greater_than(self.packet_bits)

    @staticmethod
    def _is_greater_than(packet_bits):
        return bool(Packet._p_type(packet_bits) == Packet.Type.GREATER_THAN.value)

    def is_less_than(self):
        return Packet._is_less_than(self.packet_bits)

    @staticmethod
    def _is_less_than(packet_bits):
        return bool(Packet._p_type(packet_bits) == Packet.Type.LESS_THAN.value)

    def is_equal_to(self):
        return Packet._is_equal_to(self.packet_bits)

    @staticmethod
    def _is_equal_to(packet_bits):
        return bool(Packet._p_type(packet_bits) == Packet.Type.EQUAL_TO.value)

    @staticmethod
    def make_packet(*, packet_bits=None, packet=None):
        if isinstance(packet, Packet):
            packet_bits = packet.packet_bits

        if Packet._is_sum(packet_bits):
            new_packet = SumPacket(packet_bits)
        elif Packet._is_product(packet_bits):
            new_packet = ProductPacket(packet_bits)
        elif Packet._is_min(packet_bits):
            new_packet = MinPacket(packet_bits)
        elif Packet._is_max(packet_bits):
            new_packet = MaxPacket(packet_bits)
        elif Packet._is_literal(packet_bits):
            new_packet = LiteralPacket(packet_bits)
        elif Packet._is_greater_than(packet_bits):
            new_packet = GreaterThanPacket(packet_bits)
        elif Packet._is_less_than(packet_bits):
            new_packet = LessThanPacket(packet_bits)
        elif Packet._is_equal_to(packet_bits):
            new_packet = EqualToPacket(packet_bits)
        else:
            sys.exit(f'Unsupported packet type: {Packet._p_type(packet_bits)}')

        return new_packet

    def value(self) -> (int, int, int):
        print('Sublcasses should implement value()')
        exit(2)

    def to_string(self):
        result = f'\npacket_bits: {self.packet_bits.to01()}\n'
        result += f'version: {self.version()} ({bin(self.version())})\n'
        result += f'p_type: {self.p_type()} ({bin(self.p_type())})\n'
        type_str = 'Literal' if self.is_literal() else 'Operator'
        result += f'type: {type_str}\n'
        return result


class LiteralPacket(Packet):
    VALUE_GROUP_OFFSET = Packet.TYPE_OFFSET + Packet.TYPE_LENGTH
    VALUE_GROUP_LENGTH = 5

    def __init__(self, packet_bits):
        super().__init__(packet_bits)

    def value(self) -> (int, int, int):
        value = i = 0
        bit_count = Packet.HEADER_LENGTH
        done = False
        while not done:
            value_group = self.get_value_group(i)
            value = (value << (LiteralPacket.VALUE_GROUP_LENGTH - 1)) | int(value_group[1:].to01(), 2)
            bit_count += LiteralPacket.VALUE_GROUP_LENGTH
            done = value_group[0] == 0
            i += 1
        return self.version(), bit_count, value

    def get_value_group(self, group_index):
        start_index = LiteralPacket.VALUE_GROUP_OFFSET + (LiteralPacket.VALUE_GROUP_LENGTH * group_index)
        return self.packet_bits[start_index:start_index + LiteralPacket.VALUE_GROUP_LENGTH]

    def length_bits(self):
        packet_length_bits = LiteralPacket.VALUE_GROUP_OFFSET
        done = False
        i = 0
        while not done:
            value_group = self.get_value_group(i)
            done = value_group[0] == 0
            packet_length_bits += LiteralPacket.VALUE_GROUP_LENGTH
            i += 1
        return packet_length_bits

    def to_string(self):
        result = Packet.to_string(self)
        i = 0
        done = False
        value_groups = ''
        while not done:
            value_group = self.get_value_group(i)
            value_groups += value_group.to01() + ' '
            done = value_group[0] == 0
            i += 1

        result += f'value_groups: {value_groups}\n'
        result += f'value: {self.value()}\n'
        result += f'this packet length in bits: {self.length_bits()}'
        return result


class OperatorPacket(Packet):
    MODE_OFFSET = Packet.TYPE_OFFSET + Packet.TYPE_LENGTH
    MODE_LENGTH = 1
    LENGTH_BITS_OFFSET = MODE_OFFSET + MODE_LENGTH
    LENGTH_BITS_LENGTH = 15
    LENGTH_PACKETS_OFFSET = LENGTH_BITS_OFFSET
    LENGTH_PACKETS_LENGTH = 11
    SUB_PACKETS_BIT_MODE_OFFSET = LENGTH_BITS_OFFSET + LENGTH_BITS_LENGTH
    SUB_PACKETS_PACKET_MODE_OFFSET = LENGTH_PACKETS_OFFSET + LENGTH_PACKETS_LENGTH

    def __init__(self, packet_bits):
        super().__init__(packet_bits)

    def is_bit_mode(self):
        start_index = OperatorPacket.MODE_OFFSET
        return bool(self.packet_bits[start_index] == 0)

    def is_packet_mode(self):
        return not self.is_bit_mode()

    def sub_packets_bit_length(self):
        return int(self.packet_bits[
                   OperatorPacket.LENGTH_BITS_OFFSET:OperatorPacket.LENGTH_BITS_OFFSET + OperatorPacket.LENGTH_BITS_LENGTH].to01(),
                   2)

    def sub_packets_packet_length(self):
        return int(self.packet_bits[
                   OperatorPacket.LENGTH_PACKETS_OFFSET:OperatorPacket.LENGTH_PACKETS_OFFSET + OperatorPacket.LENGTH_PACKETS_LENGTH].to01(),
                   2)

    def sub_packet_bits(self):
        if self.is_bit_mode():
            return self.packet_bits[OperatorPacket.SUB_PACKETS_BIT_MODE_OFFSET:]
        else:
            return self.packet_bits[OperatorPacket.SUB_PACKETS_PACKET_MODE_OFFSET:]

    def packet_overhead_in_bits(self):
        if self.is_bit_mode():
            return OperatorPacket.SUB_PACKETS_BIT_MODE_OFFSET + 1
        else:
            return OperatorPacket.SUB_PACKETS_PACKET_MODE_OFFSET + 1

    def length_bits(self):
        if self.is_bit_mode():
            packet_length_bits = OperatorPacket.SUB_PACKETS_BIT_MODE_OFFSET
            packet_length_bits += OperatorPacket.LENGTH_BITS_LENGTH
        else:
            packet_length_bits = OperatorPacket.SUB_PACKETS_PACKET_MODE_OFFSET
            packet_length_bits += OperatorPacket.LENGTH_PACKETS_LENGTH
        packet_length_bits += self.sub_packets_bit_length()
        return packet_length_bits

    def apply(self, operation):
        version_sum = 0
        bit_count = 0
        packet_count = 0
        values = []
        done = False
        while not done:
            sub_packet = Packet.make_packet(packet_bits=self.sub_packet_bits()[bit_count:])
            sub_version_sum, bits_processed, sub_value = sub_packet.value()
            values.append(sub_value)
            bit_count += bits_processed
            version_sum += sub_version_sum
            packet_count += 1
            if self.is_bit_mode():
                if bit_count >= self.sub_packets_bit_length():
                    done = True
            else:
                if packet_count >= self.sub_packets_packet_length():
                    done = True
        version_sum += self.version()
        if self.is_bit_mode():
            bit_count += OperatorPacket.SUB_PACKETS_BIT_MODE_OFFSET
        else:
            bit_count += OperatorPacket.SUB_PACKETS_PACKET_MODE_OFFSET

        return version_sum, bit_count, operation(values)

    def to_string(self):
        result = Packet.to_string(self)
        mode = 'Bit' if self.is_bit_mode() else 'Packet'
        result += f'mode: {mode}\n'
        length = self.sub_packets_bit_length() if self.is_bit_mode() else self.sub_packets_packet_length()
        result += f'sub-packet length: {length}\n'
        result += f'this packet length in bits: {self.length_bits()}'
        return result


class SumPacket(OperatorPacket):

    def __init__(self, packet_bits):
        super().__init__(packet_bits)

    def operation(self, values):
        return sum(values)

    def value(self) -> (int, int, int):
        return self.apply(self.operation)


class ProductPacket(OperatorPacket):

    def __init__(self, packet_bits):
        super().__init__(packet_bits)

    def operation(self, values):
        result = 1
        for value in values:
            result *= value
        return result

    def value(self):
        return self.apply(self.operation)


class MinPacket(OperatorPacket):

    def __init__(self, packet_bits):
        super().__init__(packet_bits)

    def operation(self, values):
        return min(values)

    def value(self):
        return self.apply(self.operation)


class MaxPacket(OperatorPacket):

    def __init__(self, packet_bits):
        super().__init__(packet_bits)

    def operation(self, values):
        return max(values)

    def value(self):
        return self.apply(self.operation)


class GreaterThanPacket(OperatorPacket):

    def __init__(self, packet_bits):
        super().__init__(packet_bits)

    def operation(self, values):
        return int(values[0] > values[1])

    def value(self):
        return self.apply(self.operation)


class LessThanPacket(OperatorPacket):

    def __init__(self, packet_bits):
        super().__init__(packet_bits)

    def operation(self, values):
        return int(values[0] < values[1])

    def value(self):
        return self.apply(self.operation)


class EqualToPacket(OperatorPacket):

    def __init__(self, packet_bits):
        super().__init__(packet_bits)

    def operation(self, values):
        return int(values[0] == values[1])

    def value(self):
        return self.apply(self.operation)


# def process_operator_packet(operator_packet):
#     version_sum = 0
#     bit_count = 0
#     packet_count = 0
#     value = 0
#     done = False
#     while not done:
#         sub_packet = Packet.make_packet(packet_bits=operator_packet.sub_packet_bits()[bit_count:])
#         sub_version_sum, bits_processed, value = process_packet(sub_packet)
#         bit_count += bits_processed
#         version_sum += sub_version_sum
#         packet_count += 1
#         if operator_packet.is_bit_mode():
#             if bit_count >= operator_packet.sub_packets_bit_length():
#                 done = True
#         else:
#             if packet_count >= operator_packet.sub_packets_packet_length():
#                 done = True
#     version_sum += operator_packet.version()
#     if operator_packet.is_bit_mode():
#         bit_count += OperatorPacket.SUB_PACKETS_BIT_MODE_OFFSET
#     else:
#         bit_count += OperatorPacket.SUB_PACKETS_PACKET_MODE_OFFSET
#
#     return version_sum, bit_count, value


def process_packet(packet) -> (int, int):
    # if packet.is_literal():
    #     version_sum = packet.version()
    #     bit_count = packet.length_bits()
    #     value = packet.value()
    # else:
    #     version_sum, bit_count, value = process_operator_packet(packet)
    return packet.value()


def init_data() -> bitarray:
    with open('data.txt', 'r') as data_file:
        line = data_file.readline()
    packet_bits = bitarray()
    for i in range(0, len(line), 2):
        packet_bits.extend(format(int(line[i:i+2], 16), '08b'))
    return packet_bits


def main() -> None:
    packet_bits = init_data()
    version_sum, bit_count, value = process_packet(Packet.make_packet(packet_bits=packet_bits))
    print(f'Part 1, version_sum = {version_sum}')
    print(f'Part 2, value = {value}')

    # risk_levels = expand_risk_levels()
    # do_run(2)


if __name__ == '__main__':
    main()
