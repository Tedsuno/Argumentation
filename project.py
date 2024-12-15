import argparse
from typing import List, Set, Tuple

class ArgumentationFramework:
    def __init__(self, arguments: Set[str], attacks: Set[Tuple[str, str]]):
        self.arguments = arguments
        self.attacks = attacks

    @staticmethod
    def from_file(file_path: str):
        """Parse an argumentation framework from a file."""
        arguments = set()
        attacks = set()

        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith("arg("):
                    arg = line.strip()[4:-2]
                    arguments.add(arg)
                elif line.startswith("att("):
                    attack = line.strip()[4:-2]
                    attacker, target = attack.split(',')
                    attacks.add((attacker, target))

        return ArgumentationFramework(arguments, attacks)

    def is_conflict_free(self, subset: Set[str]) -> bool:
        """Check if a subset of arguments is conflict-free."""
        for a in subset:
            for b in subset:
                if (a, b) in self.attacks:
                    return False
        return True

    def defends(self, arg: str, subset: Set[str]) -> bool:
        """Check if a subset defends an argument."""
        for attacker, target in self.attacks:
            if target == arg and attacker not in subset:
                defended = False
                for defender in subset:
                    if (defender, attacker) in self.attacks:
                        defended = True
                        break
                if not defended:
                    return False
        return True

    def is_admissible(self, subset: Set[str]) -> bool:
        """Check if a subset is admissible."""
        if not self.is_conflict_free(subset):
            return False
        for arg in subset:
            if not self.defends(arg, subset):
                return False
        return True

    def complete_extensions(self) -> List[Set[str]]:
        """Compute all complete extensions."""
        extensions = []
        for subset in self.power_set():
            if self.is_admissible(subset):
                defended = {arg for arg in self.arguments if self.defends(arg, subset)}
                if defended == subset:
                    extensions.append(subset)
        return extensions

    def stable_extensions(self) -> List[Set[str]]:
        """Compute all stable extensions."""
        extensions = []
        for subset in self.power_set():
            if self.is_conflict_free(subset):
                attacked = {target for attacker in subset for attacker, target in self.attacks}
                if attacked.union(subset) == self.arguments:
                    extensions.append(subset)
        return extensions

    def power_set(self):
        """Generate the power set of arguments."""
        from itertools import chain, combinations
        return map(set, chain.from_iterable(combinations(self.arguments, r) for r in range(len(self.arguments) + 1)))


def main():
    parser = argparse.ArgumentParser(description="Argumentation Framework Solver")
    parser.add_argument("-p", required=True, help="Problem type (e.g., SE-CO, DC-CO, etc.)")
    parser.add_argument("-f", required=True, help="Path to the file describing the argumentation framework.")
    parser.add_argument("-a", help="Argument name (for DC or DS problems).", default=None)
    
    args = parser.parse_args()

    # Load the argumentation framework
    af = ArgumentationFramework.from_file(args.f)

    # Solve the problem based on the specified type
    if args.p == "SE-CO":
        extensions = af.complete_extensions()
        print(extensions[0] if extensions else "NO")

    elif args.p == "SE-ST":
        extensions = af.stable_extensions()
        print(extensions[0] if extensions else "NO")

    elif args.p.startswith("DC") or args.p.startswith("DS"):
        if not args.a:
            print("Argument (-a) is required for DC and DS problems.")
            return

        argument = args.a
        if args.p == "DC-CO":
            print("YES" if any(argument in ext for ext in af.complete_extensions()) else "NO")

        elif args.p == "DS-CO":
            print("YES" if all(argument in ext for ext in af.complete_extensions()) else "NO")

        elif args.p == "DC-ST":
            print("YES" if any(argument in ext for ext in af.stable_extensions()) else "NO")

        elif args.p == "DS-ST":
            print("YES" if all(argument in ext for ext in af.stable_extensions()) else "NO")

    else:
        print(f"Unknown problem type: {args.p}")


if __name__ == "__main__":
    main()
