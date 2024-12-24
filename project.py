import argparse
from argumentation import Argumentation

def main():
    #Ici on parse les commandes pour les traiter en fonction de leurs arguments et options (SE-XX, ST-XX..)
    parser = argparse.ArgumentParser(description="Argumentation Solveur")
    parser.add_argument("-p", required=True)
    parser.add_argument("-f", required=True)
    parser.add_argument("-a", default=None)
    
    args = parser.parse_args()

    # On crée l'argumentation grâce à la fonction fichier_vers_arg
    af = Argumentation.fichier_vers_arg(args.f)

    # Ensuite en fonction des options on renvoie la sortie correspondante
    if args.p == "SE-CO":
        #Ici les extensions complètes
        print(sorted([sorted(ext) for ext in af.complete_extensions()]))
        #Ici les extensions stables
    elif args.p == "SE-ST":
        print(sorted([sorted(ext) for ext in af.stable_extensions()]))
    #Ici les DC et DS avec argument
    elif args.p.startswith("DC") or args.p.startswith("DS"):
        if not args.a:
            print("L'argument -a est requit")
            return
        argument = args.a
        extension_type = af.complete_extensions if "CO" in args.p else af.stable_extensions
        verification = any if "DC" in args.p else all
        print("YES" if verification(argument in ext for ext in extension_type()) else "NO")

    else:
        print(f"Problème inconnu: {args.p}")

if __name__ == "__main__":
    main()
