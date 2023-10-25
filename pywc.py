# pywc.py
# https://thecodinginterface.com/blog/python-click-cli-wc-clone/

import click


class DataRow:
    def __init__(self, name):
        self.name = name
        self.lines = 0
        self.bytes = 0
        self.words = 0
        self.chars = 0

    def output(
        self, show_lines=False, show_chars=False, show_words=False, show_bytes=False
    ):
        num_cols = sum([show_bytes, show_chars, show_lines, show_words])
        fmts = ['{:>8}'] * num_cols  # if num_cols=3 [{:>8} {:>8} {:>8}]
        fmts.append('{:<20}')
        fmt = ' '.join(fmts)

        fields = []
        if show_lines:
            fields.append(self.lines)
        if show_words:
            fields.append(self.words)
        if show_bytes:
            fields.append(self.bytes)
        if show_chars:
            fields.append(self.chars)

        fields.append(self.name)
        return fmt.format(*fields)


@click.command()
@click.argument("inputs", type=click.File("r"), nargs=-1)
@click.option("-c", help="Count bytes in each input file", is_flag=True)
@click.option("-l", help="Count lines in each input file", is_flag=True)
@click.option("-m", help="Count characters in each input file", is_flag=True)
@click.option("-w", help="Count words in each input file", is_flag=True)
def main(inputs, c, l, m, w):
    """Python clone of Unix wc program."""
    show_default = not any([c, l, m, w])
    total_row = DataRow("total")

    for file in inputs:
        row = DataRow(file.name)
        for line in file:
            # click.echo(f'{row.name:>18} -> {line}', nl=False)
            row.bytes += len(line.encode("utf-8"))
            row.lines += 1
            row.chars += len(line)
            row.words += len(
                line.strip().split()
            )  # strip gets rid of leading white spaces

        total_row.bytes += row.bytes
        total_row.lines += row.lines
        total_row.chars += row.chars
        total_row.words += row.words

        click.echo(
            row.output(
                show_lines=l or show_default,
                show_bytes=c or show_default,
                show_words=w or show_default,
                show_chars=m,
            )
        )

    if len(inputs) > 1:
        click.echo(
            total_row.output(
                show_lines=l or show_default,
                show_bytes=c or show_default,
                show_words=w or show_default,
                show_chars=m,
            )
        )


if __name__ == "__main__":
    main()
