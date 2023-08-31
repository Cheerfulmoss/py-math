GATE_INS = dict[str: bool]

INPUTS = list[str]
OUTPUTS = list[str]
GATES = list[list[str]]


class LogicGate:
    _calc_cache = NotImplementedError
    SYMBOL_REG = {
        "or": "+",
        "and": "*",
        "xor": "^",
        "not": "~",
    }

    def __init__(self, inputs: INPUTS, outputs: OUTPUTS) -> None:
        self.inputs = inputs
        self.outputs = outputs

        self.input_count = len(self.inputs)
        self.output_count = len(self.outputs)

        self._set_name()
        self._set_symbol()

    def __str__(self) -> str:
        return f"{self.inputs[0]}{self.symbol}{self.inputs[1]}"

    def __repr__(self) -> str:
        return f"{self.name}(inputs={self.inputs}, outputs={self.outputs})"

    def __contains__(self, item) -> bool:
        return item in self.inputs

    def _set_name(self) -> None:
        self.name = self.__class__.__name__

    def _set_symbol(self) -> None:
        self.symbol = self.SYMBOL_REG.get(self.__class__.__name__.lower(),
                                          NotImplementedError)

    def _run_logic(self, inputs: GATE_INS) -> bool | int:
        return NotImplementedError

    def run(self, inputs: GATE_INS) -> bool | int:
        cache_key = tuple(inputs.values())
        result = self._calc_cache.get(cache_key)
        if result is None:
            result = self._run_logic(inputs)
            self._calc_cache[cache_key] = result
        return result

    def clear_cache(self):
        self._calc_cache.clear()


class AND(LogicGate):
    _calc_cache = {}

    def _run_logic(self, inputs: GATE_INS) -> bool | int:
        output = inputs[self.inputs[0]]

        for input_g in self.inputs[1:]:
            output &= inputs[input_g]

        return output


class OR(LogicGate):
    _calc_cache = {}

    def _run_logic(self, inputs: GATE_INS) -> bool | int:
        output = inputs[self.inputs[0]]

        for input_g in self.inputs[1:]:
            output |= inputs[input_g]

        return output


class XOR(LogicGate):
    _calc_cache = {}

    def _run_logic(self, inputs: GATE_INS) -> bool | int:
        output = inputs[self.inputs[0]]

        for input_g in self.inputs[1:]:
            output ^= inputs[input_g]

        return output


class NOT(LogicGate):
    _calc_cache = {}

    def _run_logic(self, inputs: GATE_INS) -> bool | int:
        return int(not inputs[self.inputs[0]])


class Circuit:
    """Represents a circuit composed of logic gates.

    This class constructs a circuit from a list of gate operations and provides
    methods to interact with and simulate the circuit.

    Attributes:
        OPERATIONS (dict[str, LogicGate]): A dictionary mapping gate symbols to
            their corresponding classes.
        inputs (list[str]): List of input identifiers for the circuit.
        outputs (list[str]): List of output identifiers for the circuit.
        layers (dict[str: list[LogicGate]]): Dictionary containing gate
            layers in the circuit.

    Methods:
        construct_circuit(): Construct the circuit layers and retrieves
            inputs, layers and outputs. This is run on object initialisation.
    """
    OPERATIONS = {
        subclass([], []).symbol: subclass
        for subclass in LogicGate.__subclasses__()
    }

    def __init__(self, gates: GATES):
        """Initialises a Circuit instance.

        Args:
            gates (list[list[str]]): List of gate operations to construct the
                circuit.
        """
        self._gates = gates
        self.inputs, self.layers, self.outputs = self.construct_circuit()

    def construct_circuit(self) -> tuple[INPUTS, dict[str, LogicGate], OUTPUTS]:
        """Constructs the circuit layers and retrieves inputs, layers, and
            outputs.

        Returns:
            tuple: A tuple containing inputs, layers, and outputs of the
                circuit.
        """
        inputs = list()
        layers = dict()
        outputs = list()

        for layer_num, layer in enumerate(self._gates):
            for operation in layer:
                equa, output = operation.split("=")

                # Get inputs and outputs
                if equa == output:
                    if layer_num != len(self._gates) - 1:
                        inputs.append(equa)
                    else:
                        outputs.append(equa)
                    continue

                for operation_signature in self.OPERATIONS:
                    if operation_signature in equa:
                        gate_ins = tuple(equa.split(operation_signature))
                        gate = self.OPERATIONS[operation_signature](
                            gate_ins, (output,)
                        )

                        # Append the gate to the appropriate layer
                        layers.setdefault(
                            f"layer-{layer_num}", []).append(gate)
                        break

        return inputs, layers, outputs
