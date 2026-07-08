from nbtlib import Parser, List, tokenize


class FixedParser(Parser):
    def __init__(self, token_stream):
        self.next_token = None
        self.last_token = None
        super().__init__(token_stream)

    def revert_token(self):
        if not self.last_token:
            raise Exception("Unable to revert token")

        self.next_token = self.current_token
        self.current_token = self.last_token
        self.token_span = self.current_token.span
        self.last_token = None

    def next(self):
        self.last_token = self.current_token
        if self.next_token is None:
            res = super().next()
            # print("current token:" + str(self.current_token))
            return res
        self.current_token = self.next_token
        self.next_token = None
        self.token_span = self.current_token.span

    def collect_tokens_until(self, token_type):
        """
        Handle trailing commas in dictionaries
        """
        tokens = super().collect_tokens_until(token_type)
        if token_type != "CLOSE_COMPOUND":
            yield from tokens

        for t in tokens:
            if self.current_token.type == token_type:
                return
            yield t

    def parse_list(self):
        """
        Handle indexed snbt lists
        example: [0: "test", 1: "test 2"]
        example2: [0: 1B, 1: 2B, 2: 3B]

        Defer back to parse_list() for non-indexed lists
        """
        l = None
        self.next() # get token after [
        if self.current_token.type != "NUMBER":
            self.revert_token()
            return super().parse_list()

        self.next() # get token after [0
        if self.current_token.type != "COLON":
            self.revert_token()
            l = List([self.parse()])
            l += super().parse_list()
            return l
        self.revert_token() # go back to [0
        isKey = True

        for _ in self.collect_tokens_until("CLOSE_BRACKET"):
            # after parsing, we read the next token
            # so we have to check if the previous token was a comma
            if self.last_token.type == "COMMA":
                isKey = True

            # skip key and colon
            if isKey and self.current_token.type == "NUMBER":
                self.next()
                self.next()
                isKey = False

            if self.current_token.type == "CLOSE_BRACKET":
                return l
            elif self.current_token.type == "COLON":
                isKey = False
                self.next()

            elem = self.parse()
            if l is None:
                l = List([elem])
            else:
                l.append(elem)
        return l

    def parse_invalid(self):
        print("TEST")


# this is just nbtlib#parse_nbt but using the FixedParser() instead of Parser()
def parse_nbt(literal):
    """Parse a literal nbt string and return the resulting tag."""
    parser = FixedParser(tokenize(literal))
    tag = parser.parse()

    cursor = parser.token_span[1]
    leftover = literal[cursor:]

    if leftover.strip():
        parser.token_span = cursor, cursor + len(leftover)
        raise parser.error(f"Expected end of string but got {leftover!r}")

    return tag


def test():
    print("a")
    print(parse_nbt("""[0: "test", 1: "test 2"]"""))
    print("b")
    print(parse_nbt("[0: 1.25, 1: 2.25,2: 3.25]"))


if __name__ == "__main__":
    test()
