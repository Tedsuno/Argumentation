from project import ArgumentationFramework  # Assurez-vous que le fichier contenant la classe est importé correctement.

def test_is_conflict_free():
    af = ArgumentationFramework({"a", "b", "c", "d", "e"}, {("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"), ("e", "a")})
    print(af.is_conflict_free({"a", "b"}))

# Un ensemble S ⊆ A est sans conflit (cf) si aucun argument dans S n’attaque un autre argument de S

def test_defends():
    af = ArgumentationFramework({"a", "b", "c", "d", "e"}, {("a", "b"), ("b", "c"), ("c", "d"), ("d", "e")}) 

    # Test 1 : {a3, a4} défend a1
    print(af.defends("a", {"a"}))  # True

def test_is_admissible():
    af = ArgumentationFramework({"a", "b", "c", "d", "e"}, {("a", "b"), ("b", "c"), ("c", "d"), ("d", "c")})

    test_sets = [{"a", "c"}]
    
    for s in test_sets:
        print(f"\nTesting set {s}:")
        result = af.is_admissible(s)
        print(f"Is admissible: {result}")

def test_complete_extensions():
    # Créer un système d'argumentation simple
    af = ArgumentationFramework(
        arguments={"a", "b", "c", "d"},
        attacks={("a", "b"), ("b", "c"), ("c", "d"), ("d", "c")}
    )

    # Calculer les extensions complètes
    extensions = af.complete_extensions()

    # Afficher les extensions trouvées
    print("Extensions complètes trouvées:")
    for ext in extensions:
        print(ext)
    
    #s'attaque pas entre eux
    #défend tout ses arguments
    #contient dans l'ensemble tout les arguments qui se défende

    # Vérifier les résultats attendus
    expected_extensions = [set(), {"a"}, {"a", "c"}]
    
    if set(map(frozenset, extensions)) == set(map(frozenset, expected_extensions)):
        print("\nTest réussi: Les extensions complètes sont correctes.")
    else:
        print("\nTest échoué: Les extensions complètes ne correspondent pas aux résultats attendus.")
        print("Extensions attendues:", expected_extensions)

if __name__ == "__main__":
    #test_is_conflict_free()
    print("---------------")
    test_defends()
    print("---------------")
    #test_is_admissible()
    print("---------------")
    test_complete_extensions()
