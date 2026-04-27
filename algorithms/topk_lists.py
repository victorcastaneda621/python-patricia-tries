from __future__ import annotations
from typing import List, Tuple, Iterable, Set

def compute_closure(node_items: List[int], intersection: List[int]) -> Set[int]:
    return set(node_items) | set(intersection)

def extract_top_k(self, list, max_k, k) -> List[Tuple[Set[int], int]]:
        closed_sets = {}

        for node in trie.nodes_postorder: # list

            # obtenemos el closure del nodo
            closure = compute_closure(node.items, node.intersection)

            # soporte: número de transacciones que pasan por este nodo
            support = node.count

            # filtrar singletons si está desactivado
            if not self.mine_singletons and len(closure) == 1:
                continue

            key = frozenset(closure)

            # mantener mayor soporte si aparece más de una vez
            if key not in closed_sets or closed_sets[key] < support:
                closed_sets[key] = support

        # Ordenar por soporte descendente
        sorted_closed = sorted(
            [(set(items), sup) for items, sup in closed_sets.items()],
            key=lambda x: x[1],
            reverse=True
        )

        # devolver los k mejores
        return sorted_closed[: self.k]

def topk_lists(k: int, mine_singletons: bool):

    # --------------------------------------------------------
    #                API PRINCIPAL
    # --------------------------------------------------------

    def fit(self, transactions: Iterable[Iterable[int]]) -> List[Tuple[Set[int], int]]:
        """
        Ejecuta el minado top‑k sobre una lista de transacciones.
        Acepta transacciones como listas o sets.
        """

        # 1. Normalizar transacciones
        tx = normalize_transactions(transactions)

        if not tx:
            return []

        # 2. Construir Patricia Trie
        trie = PatriciaTrie()
        for t in tx:
            trie.insert(t)

        # 3. Asignar IDs y calcular intersecciones
        trie.assign_ids_and_intersections()

        # 4. Extraer itemsets cerrados y ordenarlos por soporte
        return self._extract_top_k(trie)