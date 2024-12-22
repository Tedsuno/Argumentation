import argparse
from typing import List, Set, Tuple

class ArgumentationFramework:
    def __init__(self, arguments: Set[str], attacks: Set[Tuple[str, str]]):
        self.arguments = arguments
        self.attacks = attacks

#Exemple: af = ArgumentationFramework({"a", "b", "c"}, {("a", "b"), ("b", "c")})

    @staticmethod
    def from_file(file_path: str):
        """Parse an argumentation framework from a file."""
        arguments = set()
        attacks = set()

        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("arg(") and line.endswith(")."):
                    arg = line[4:-2].strip()
                    arguments.add(arg)
                elif line.startswith("att(") and line.endswith(")."):
                    attack = line[4:-2].strip()
                    attacker, target = attack.split(',')
                    attacks.add((attacker.strip(), target.strip()))

        return ArgumentationFramework(arguments, attacks)




    def is_conflict_free(self, subset: Set[str]) -> bool:
        """Check if a subset of arguments is conflict-free."""
        for a in subset:
            for b in subset:
                if (a, b) in self.attacks:
                    return False
        return True

#af = ArgumentationFramework({"a", "b", "c"}, {("a", "b"), ("b", "c")})
#print(af.is_conflict_free({"a", "c"}))  # True
#print(af.is_conflict_free({"a", "b"}))  # False
#Sous-ensemble {a, c} : Aucun argument n’attaque l’autre, donc sans conflit.
#Sous-ensemble {a, b} : a attaque b, donc pas sans conflit.

    def defends(self, arg: str, subset: Set[str]) -> bool: #est-ce que l'ensemble subset défend arg
        """Check if a subset defends an argument."""
        #nb_attaquant = 0
        for attacker, target in self.attacks:

            # Vérifier si l'argument arg est la cible d'une attaque
            if target == arg:
                #nb_attaquant += 1
                # Afficher les conditions vérifiées
                
                # Vérifier si un défenseur attaque l'attaquant
                if not any((defender, attacker) in self.attacks for defender in subset):
                    return False
        #if nb_attaquant == 0:
            #return False
        return True
        


#af = ArgumentationFramework({"a", "b", "c"}, {("a", "b"), ("b", "c")})
#print(af.defends("b", {"a"}))  # True
#print(af.defends("c", {"a"}))  # False
#{a} défend b : b est attaqué par a, mais a est présent dans le sous-ensemble pour le défendre.
#{a} ne défend pas c : c est attaqué par b, mais a n’attaque pas b.


    def is_admissible(self, subset: Set[str]) -> bool:
        """Check if a subset is admissible."""
        if not self.is_conflict_free(subset):
            return False
        for arg in subset:
            if not self.defends(arg, subset):
                return False
        return True

#af = ArgumentationFramework({"a", "b", "c"}, {("a", "b"), ("b", "c")})
#print(af.is_admissible({"a"}))  # True
#print(af.is_admissible({"b"}))  # False
#{a} : Sans conflit, défend tous ses arguments → Admissible.
#{b} : Sans conflit mais ne défend pas b contre l’attaque de a → Pas admissible.

    def complete_extensions(self) -> List[Set[str]]:
        """Compute all complete extensions."""
        extensions = []
        for subset in self.power_set():
            if self.is_admissible(subset):
                defended = set(arg for arg in self.arguments if self.defends(arg, subset))
                #print(f"Subset: {subset}, Defended: {defended}")  # Affiche le sous-ensemble et les arguments défendus
                if subset == defended:
                    extensions.append(subset)
        return extensions

#af = ArgumentationFramework({"a", "b", "c"}, {("a", "b"), ("b", "c")})
#print(af.complete_extensions())  # [{'a'}, {'a', 'c'}]
#{a} : Admissible et défend tous les arguments qu'il doit défendre.
#{a, c} : Admissible et inclut tous les arguments qu'il défend.
#{b} ou {b, c} : Pas admissibles.


    def stable_extensions(self) -> List[Set[str]]:
        """Compute all stable extensions."""
        extensions = []
        for subset in self.power_set():
            if self.is_conflict_free(subset):  # Vérifie si l'ensemble est sans conflit
                # Arguments attaqués par le sous-ensemble
                attacked = {target for attacker, target in self.attacks if attacker in subset}
                # Vérifie si tout argument non dans subset est attaqué
                if all(arg in attacked for arg in self.arguments - subset):
                    extensions.append(subset)
        return extensions


#af = ArgumentationFramework({"a", "b", "c"}, {("a", "b"), ("b", "c")})
#print(af.stable_extensions())  # [{'a', 'c'}]
#{a, c} : Sans conflit et attaque tous les arguments qui ne sont pas dans {a, c}.
#{a} : N’attaque pas c, donc pas stable.



    def power_set(self):
        """Generate the power set of arguments."""
        from itertools import chain, combinations
        return map(set, chain.from_iterable(combinations(self.arguments, r) for r in range(len(self.arguments) + 1)))

#af = ArgumentationFramework({"a", "b"}, set())
#print(list(af.power_set()))
#Sortie : [set(), {'a'}, {'b'}, {'a', 'b'}]
#Ce que cela fait : Génère tous les sous-ensembles possibles de {a, b}.



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
        # Trier uniquement les éléments à l'intérieur de chaque ensemble
        sorted_extensions = [sorted(ext) for ext in extensions]
        sorted_extensions.sort()
        print(sorted_extensions)
        #print(extensions[0] if extensions else "NO")

    elif args.p == "SE-ST":
        extensions = af.stable_extensions()
        # Convertir chaque ensemble en une liste triée
        sorted_extensions = [sorted(ext) for ext in extensions]
        # Trier globalement les ensembles pour un ordre cohérent
        sorted_extensions.sort()
        print(sorted_extensions)


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


