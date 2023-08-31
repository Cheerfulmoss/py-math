from gates import Circuit
import cProfile


class LogicSim:
    def __init__(self, gates: list[list[str]]):
        self._circuit = Circuit(gates=gates)

    def get_circuit(self):
        return self._circuit

    def simulate(self, inputs: dict[str: bool]):
        layer_outs = inputs

        for layer, data in self._circuit.layers.items():
            layer_outs = self._sim_layer(data, layer_outs)

        return {key: value for key, value in layer_outs.items() if key in
                self._circuit.outputs}

    def _sim_layer(self, layer_data: list, layer_inputs: dict[str: bool]):
        layer_out = {}
        for gate in layer_data:

            values = {}
            for input_g in gate.inputs:
                if input_g in layer_inputs:
                    values[input_g] = layer_inputs[input_g]

            layer_out[gate.outputs[0]] = gate.run(values)

        layer_out.update(layer_inputs)

        return layer_out

    def logic_table(self) -> dict[tuple: list]:
        combs_n = 2 ** len(self._circuit.inputs)

        header = ("| " +
                  " | ".join(self._circuit.inputs + self._circuit.outputs) +
                  " |")
        border = "|" + "-" * (len(header) - 2) + "|"

        print(f"{border}\n{header}\n{border}")
        for comb in range(combs_n):
            bin_rep = f"{bin(comb)[2:]:0>{combs_n.bit_length() - 1}}"
            dictionary_in = {
                key: int(bin_rep[i]) for i, key in enumerate(
                    self._circuit.inputs)
            }
            output = self.simulate(dictionary_in)

            print(
                "| " +
                "   ".join(str(x) for x in dictionary_in.values()) +
                " | " + "   ".join(str(y) for y in output.values()) +
                " | " + f"{comb}"
            )
        print(border)


def main():
    examp = [
        ["A=A", "B=B", "C=C"],
        ["A*B=D", "B+C=E"],
        ["D+E=F", "A*E=G"],
        ["F*G=H", "A^B=I", "C~C=J"],
        ["H=H", "I=I", "J=J"]
    ]

    LogicSim(examp).logic_table()
    LogicSim(examp)


if __name__ == "__main__":
    cProfile.run("main()")
