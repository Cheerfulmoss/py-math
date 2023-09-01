from gates import Circuit
import cProfile


class LogicSim:
    def __init__(self, gates: list[list[str]]):
        self._circuit = Circuit(gates=gates)

    def get_circuit(self):
        return self._circuit

    def simulate(self, inputs: dict[str: bool], verbose: bool = False):
        layer_outs = inputs

        for layer, data in self._circuit.layers.items():
            layer_outs = self._sim_layer(data, layer_outs)

        if verbose:
            return (
                {key: value for key, value in layer_outs.items() if key in
                 self._circuit.inputs},
                {key: value for key, value in list(layer_outs.items())[::-1]
                 if key not in self._circuit.outputs and
                 key not in self._circuit.inputs},
                {key: value for key, value in layer_outs.items() if key in
                 self._circuit.outputs})

        return (
            {key: value for key, value in layer_outs.items() if key in
             self._circuit.inputs},
            {key: value for key, value in layer_outs.items() if key in
             self._circuit.outputs})

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

    def logic_table(self, verbose: bool) -> dict[tuple: list]:
        combs_n = 2 ** len(self._circuit.inputs)
        row_outs = list()

        for comb in range(combs_n):
            bin_rep = f"{bin(comb)[2:]:0>{combs_n.bit_length() - 1}}"
            dictionary_in = {
                key: int(bin_rep[i]) for i, key in enumerate(
                    self._circuit.inputs)
            }
            output = self.simulate(dictionary_in, verbose=verbose)
            row_outs.append(output)

        header_setter = row_outs[0]
        header = []

        for out in header_setter:
            header.append("   ".join(list(out.keys())))

        header = f"| {' | '.join(header)} |"
        border = f"|{'-' * (len(header) - 2)}|"

        print(f"{border}\n{header}\n{border}")

        for row_i, row_d in enumerate(row_outs):
            row = []
            for out in row_d:
                row.append("   ".join(str(x) for x in out.values()))
            row = f"| {' | '.join(row)} | {row_i}"
            print(row)
        print(border)


def main():
    examp = [
        ["A=A", "B=B", "C=C", "D=D", "E=E"],
        ["A+B=F", "D+E=G", "C^B=H", "C^D=I"],
        ["I~I=J"],
        ["F*H=K", "G*J=L"],
        ["L+K=M"],
        ["M=M"]
    ]

    x = LogicSim(examp)
    x.logic_table(verbose=True)
    x.logic_table(verbose=False)


if __name__ == "__main__":
    cProfile.run("main()")
