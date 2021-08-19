import math
import copy
import argparse
import doctest
from os import listdir
from os.path import isfile, join
from graphe import *


def charger_noms(graphe: Graphe, lines):
    for line in lines:
        if line == "# stations\n":
            continue
        elif line == "# connexions\n":
            break
        value = line.split(":")[0]
        nom = line.split(":")[1]
        graphe.ajouter_sommet(int(value))
        graphe.ajouter_nom(int(value), nom.rstrip(nom[-1]))


def charger_reseaux(graphe: Graphe, lines: list, value):
    read = False
    for line in lines:
        if read == False:
            if line == "# connexions\n":
                read = True
            continue
        elem1 = line.split("/")[0]
        elem2 = line.split("/")[1]
        graphe.ajouter_arete(int(elem1), int(elem2), value)


def charger_donnees(graphe: Graphe, fichier):
    value = fichier.split(".")[0]
    f = open(fichier, "r")
    lines = f.readlines()
    f.close()
    charger_noms(graphe, lines)
    charger_reseaux(graphe, lines, value)


def degre(graphe: Graphe, sommet, parent):
    count = 0
    for voisins in graphe.voisins(sommet):
        if parent[voisins] == sommet:
            count += 1
    return count


def numerotation(graphe: Graphe):
    debut = dict()
    parent = dict()
    ancetre = dict()
    instant = 0
    for v in sorted(graphe.sommets()):
        debut[v] = 0
        parent[v] = None
        ancetre[v] = math.inf

    def numRec(s):
        nonlocal instant
        instant = instant + 1
        debut[s] = ancetre[s] = instant
        for t in graphe.voisins(s):
            if debut[t] != 0:
                if parent[s] != t:
                    ancetre[s] = min(ancetre[s], debut[t])
            else:
                parent[t] = s
                numRec(t)
                ancetre[s] = min(ancetre[s], ancetre[t])
    for v in sorted(graphe.sommets()):
        if debut[v] == 0:
            numRec(v)
    return debut, parent, ancetre


def pointsArticulation(graphe: Graphe, debut, parent, ancetre):
    articulation = []
    racine = []
    for v in sorted(graphe.sommets()):
        if parent[v] == None:
            racine.append(v)
    for depart in racine:
        if degre(graphe, depart, parent) >= 2:
            articulation.append(depart)
    racine.append(None)
    for v in sorted(graphe.sommets()):
        if parent[v] not in racine and ancetre[v] >= debut[parent[v]]:
            articulation.append(parent[v])
    return set(articulation)


def points_articulation(g):
    num = numerotation(g)
    return pointsArticulation(g, num[0], num[1], num[2])


def ponts(g):
    debut, parent, ancetre = numerotation(g)
    ponts = []
    for sommet in sorted(g.sommets()):
        if parent[sommet] != None:
            if ancetre[sommet] > debut[parent[sommet]]:
                ponts.append((parent[sommet], sommet))
    return ponts


def parcours(g: Graphe, pont, sommet, feuille):
    for val in g.voisins(sommet):
        if val == pont[1] or val == pont[0] or val in feuille:
            continue
        elif val not in feuille:
            feuille.append(val)
            parcours(g, pont, val, feuille)


def detection_feuille(g: Graphe, pont, sommet):
    feuille = []
    feuille.append(sommet)
    parcours(g, pont, sommet, feuille)
    return sorted(feuille)


def verif_feuille(g: Graphe, feuille, pont):
    for val in feuille:
        for val2 in ponts(g):
            if val in val2 and val2 != pont:
                feuille = None
                break
    return feuille


def retrouveFeuille(csp):
    return sorted(csp, reverse=True)[0]


def amelioration_ponts(g: Graphe):
    csp1 = dict()
    csp2 = dict()
    feuille = []
    arrete = []
    for pont in ponts(g):
        csp1 = detection_feuille(g, pont, pont[0])
        csp2 = detection_feuille(g, pont, pont[1])
        csp1 = verif_feuille(g, csp1, pont)
        csp2 = verif_feuille(g, csp2, pont)
        if csp1 != None:
            feuille.append(retrouveFeuille(csp1))
        if csp2 != None:
            feuille.append(retrouveFeuille(csp2))
    for i in range(1, len(feuille)):
        arrete.append((feuille[i - 1], feuille[i]))
    return sorted(arrete)


def recupFils(graphe: Graphe, sommet, parent):
    fils = []
    for som in graphe.sommets():
        if parent[som] == sommet:
            fils.append(som)
    return fils


def amelioration_points_articulation(g):
    cpy = Graphe()
    _, parent, ancetre = numerotation(g)
    fils = []
    arrete = []
    racine = []
    cpy = copy.deepcopy(g)
    arrete = amelioration_ponts(g)
    for u, v in arrete:
        cpy.ajouter_arete(u, v, 'None')
    if(len(points_articulation(cpy)) == 0):
        return sorted(arrete)
    pntArti = sorted(points_articulation(cpy), reverse=True)
    for v in sorted(g.sommets()):
        if parent[v] == None:
            racine.append(v)
    for pnt in pntArti:
        fils = recupFils(g, pnt, parent)
        if pnt in racine:
            arrete.append((fils[0], fils[1]))
        else:
            if len(fils) == 1 and fils[0] not in pntArti:
                arrete.append((racine[0], fils[0]))
            else:
                for v in fils:
                    if v not in pntArti and ancetre[v] != ancetre[pnt]:
                        arrete.append((racine[0], v))
    return sorted(arrete)


def displayStations(g):
    print()
    station = g.sommets()
    noms = sorted(
        list(map(lambda a: g.nom_sommet(a) + " (" + str(a) + ")", station)))
    print("Le réseau contient les " +
          str(g.nombre_sommets()) + " stations suivantes:")
    print()
    for u in noms:
        print(u)
    print()


def displayPont(g):
    print()
    pont = ponts(g)
    noms = sorted(list(map(lambda a: g.nom_sommet(
        a[0]) + " -- " + g.nom_sommet(a[1]), pont)))
    if len(pont) == 0:
        print("Le réseau ne contient pas de pont")
    else:
        print("Le réseau contient les " + str(len(pont)) + " ponts suivants:")
    for u in noms:
        print('\t- ' + str(u))
    print()


def displayPointArti(g):
    print()
    point = points_articulation(g)
    noms = sorted(list(map(lambda a: g.nom_sommet(a), point)))
    if len(point) == 0:
        print("Le réseau ne contient pas de points d'articulation.")
    else:
        print("Le réseau contient les " + str(len(point)) +
              " points d'articulations suivants:")
    for i in range(len(noms)):
        print('\t' + str(i + 1) + " : " + str(noms[i]))
    print()


def displayPointArtiAmelio(g):
    print()
    arrete = amelioration_points_articulation(g)
    noms = sorted(list(map(lambda a: g.nom_sommet(
        a[0]) + " -- " + g.nom_sommet(a[1]), arrete)))
    print("On peut éliminer tous les points d'articulations du réseau en rajoutant les " +
          str(len(arrete)) + " arêtes suivantes :")
    for u in noms:
        print('\t- ' + str(u))
    print()


def displayPontAmelio(g):
    print()
    arrete = amelioration_ponts(g)
    noms = sorted(list(map(lambda a: g.nom_sommet(
        a[0]) + " -- " + g.nom_sommet(a[1]), arrete)))
    print("On peut éliminer tous les ponts du réseau en rajoutant les " +
          str(len(arrete)) + " arêtes suivantes :")
    for u in noms:
        print('\t- ' + str(u))
    print()


def parserAddArgument(parser):
    parser.add_argument("--metro", nargs='*', help="load line of metro")
    parser.add_argument("--rer", nargs='*', help="load line of rer")
    parser.add_argument(
        "--liste-stations", help="displays the list of network stations with their identifier sorted in order alphabetical", action="store_true")
    parser.add_argument(
        "--articulations", help="displays the articulation points of the network that has been loaded", action="store_true")
    parser.add_argument(
        "--ponts", help="displays the bridges of the network that has been loaded", action="store_true")
    parser.add_argument("--ameliorer-articulations",
                        help="displays the articulation points of the network that has been loaded,as well as the edges to be added so that these stations are no longer points of articulation", action="store_true")
    parser.add_argument(
        "--ameliorer-ponts", help="displays the bridges of the network that has been loaded, as well as the edges to addso that these edges are no longer bridges.", action="store_true")


def loadRerOrMetro(g, args, mode):
    if args != None:
        if args == []:
            fichiers = [f for f in listdir('.') if isfile(join('.', f))]
            for f in fichiers:
                if f.startswith(mode.upper()):
                    charger_donnees(g, f)
            print("Chargement de toutes les lignes de " +
                  str(mode) + " ... terminé.")
        else:
            for val in args:
                name = mode.upper() + '_' + str(val) + ".txt"
                charger_donnees(g, name)
            print("Chargement des lignes " + str(sorted(args)) +
                  " de " + str(mode) + " ... terminé.")
        print("Le réseau contient " + str(g.nombre_sommets()) +
              " sommets et " + str(g.nombre_aretes()) + " arêtes.")


def gestionArgs(g, parser):
    parserAddArgument(parser)
    args = parser.parse_args()
    if args.metro != None:
        loadRerOrMetro(g, args.metro, 'metro')
    if args.rer != None:
        loadRerOrMetro(g, args.rer, 'rer')
    if args.liste_stations:
        displayStations(g)
    if args.articulations:
        displayPointArti(g)
    if args.ponts:
        displayPont(g)
    if args.ameliorer_articulations:
        displayPointArtiAmelio(g)
    if args.ameliorer_ponts:
        displayPontAmelio(g)


def main():
    doctest.testmod()
    parser = argparse.ArgumentParser()
    g = Graphe()
    gestionArgs(g, parser)


if __name__ == "__main__":
    main()
