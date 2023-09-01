"""
Alexander Burow - 2 September 2023

License: GPL3

There is no error checking.
"""

from gates import Circuit
import cProfile


class LogicSim:
    def __init__(self, gates: list[list[str]]):
        self._circuit = Circuit(gates=gates)
        self.sim_list = None
        self.sim_state = None

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

    def full_sim(self, verbose: bool = False) -> None:
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

        self.sim_state = verbose
        self.sim_list = tuple(row_outs)

    def _basic_table(self, verbose: bool, row_filter=None,
                     title: str = "Unspecified"):
        if self.sim_list is None or (self.sim_state != verbose and verbose):
            self.full_sim(verbose=verbose)
            local_sim_list = self.sim_list
        elif self.sim_state != verbose:
            local_sim_list = tuple(
                (sim_state[0], sim_state[2]) for sim_state in self.sim_list
            )
        else:
            local_sim_list = self.sim_list

        header_setter = local_sim_list[0]
        header = []

        for out in header_setter:
            header.append("   ".join(list(out.keys())))

        header_content = " | ".join(header)

        pad = max(len(header_content), len(title))

        header = f"| {header_content:^{pad}} |"
        border = f"|{'-' * (pad+2)}|"
        ttitle = f"| {title:^{pad}} |"

        print(f"{border}\n{ttitle}\n{border}\n{header}\n{border}")

        if row_filter is None:
            row_filter = lambda row: True

        for row_i, row_d in enumerate(local_sim_list):
            if row_filter(row_d):
                row = []
                for out in row_d:
                    row.append("   ".join(str(x) for x in out.values()))

                row_content = " | ".join(row)
                row = f"| {row_content:^{pad}} | {row_i}"
                print(row)
        print(border)

    def ones_table(self, verbose: bool):
        self._basic_table(verbose=verbose,
                          row_filter=lambda row: any(row[-1].values()),
                          title="Ones Table")

    def uniform_ones_table(self, verbose: bool):
        self._basic_table(verbose=verbose,
                          row_filter=lambda row: all(row[-1].values()),
                          title="Uniform Ones Table")

    def uniform_zeros_table(self, verbose: bool):
        self._basic_table(verbose=verbose,
                          row_filter=lambda row: not any(row[-1].values()),
                          title="Uniform Zeros Table")

    def zeros_table(self, verbose: bool):
        self._basic_table(verbose=verbose,
                          row_filter=lambda row: not all(row[-1].values()),
                          title="Zeros Table")

    def logic_table(self, verbose: bool) -> None:
        self._basic_table(verbose=verbose,
                          title="Complete Logic Table")


def main():
    examp1 = [
        ["A=A", "B=B", "C=C", "D=D", "E=E"],
        ["A+B=F", "D+E=G", "C^B=H", "C^D=I"],
        ["I~I=J"],
        ["F*H=K", "G*J=L"],
        ["L+K=M", "A*K=N"],
        ["M=M", "N=N"]
    ]

    x = LogicSim(examp1)
    x.logic_table(verbose=True)
    x.logic_table(verbose=False)
    x.ones_table(verbose=True)
    x.ones_table(verbose=False)
    x.zeros_table(verbose=True)
    x.zeros_table(verbose=False)


if __name__ == "__main__":
    cProfile.run("main()")
