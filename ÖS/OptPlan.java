/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.kandidatprojektv2;

import java.util.*;

/**
 * @author joakimharrieson
 */
public class OptPlan {

    // initieras parameterar/variabler
    private List<Vertex> nodes;
    private List<Edge> edges;
    private DataStore ds;

    private LinkedList<Vertex>[] allPaths = new LinkedList[100];

    // kopplar sig samman till DataStore
    public OptPlan(DataStore ds) {
        this.ds = ds;
    }

    public boolean contains(int[] array, int target) {
        for (int element : array) {
            if (element == target) {
                return true;
            }
        }
        return false;
    }

    // Funktion som används för att generera alla kombinationer av noder baserat på indata.
    public static List<List<Integer>> generateCombinations(int[] nodes) {
        List<List<Integer>> result = new ArrayList<>();
        boolean[] used = new boolean[nodes.length];
        List<Integer> current = new ArrayList<>();
        generate(nodes, used, current, result);
        return result;
    }

    private static void generate(int[] nodes, boolean[] used, List<Integer> current, List<List<Integer>> result) {
        if (current.size() == nodes.length) {
            result.add(new ArrayList<>(current));
            return;
        }

        for (int i = 0; i < nodes.length; i++) {
            if (!used[i]) {
                used[i] = true;
                current.add(nodes[i]);
                generate(nodes, used, current, result);
                current.remove(current.size() - 1);
                used[i] = false;
            }
        }
    }

    // Adderad kod
    public void createPlan() {

        nodes = new ArrayList<Vertex>();
        edges = new ArrayList<Edge>();

        int gridsizeX = 22;
        int gridsizeY = 10;

        // Set up network
        for (int i = 1; i <= gridsizeX * gridsizeY; i++) {
            Vertex location = new Vertex("" + i, "Nod #" + i);
            nodes.add(location);
        }

        // Gör om alla noder till X och Y koordinater
        int count = 0;
        for (int i = 0; i < 10; i++) {
            for (int j = 1; j <= 22; j++) {
                ds.nodeY[count] = 30 * i;
                count = count + 1;
            }
        }

        count = 0;
        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 22; j++) {
                ds.nodeX[count] = 30 * j;
                count = count + 1;
            }
        }

        //Skapar shelfPick noder baserat på väderstreck på plockplacering
        int[] shelfPick = new int[ds.ownnoShelves];
        System.out.println(ds.ownnoShelves);
        for (int t = 0; t < ds.ownnoShelves; t++) {
            if (ds.ownshelfDir[t].equals("N")) {
                shelfPick[t] = ds.ownshelfX[t] / 30 + ((ds.ownshelfY[t] + 30) / 30) * gridsizeX;
            }
            if (ds.ownshelfDir[t].equals("S")) {
                shelfPick[t] = ds.ownshelfX[t] / 30 + ((ds.ownshelfY[t] - 30) / 30) * gridsizeX;
            }
            if (ds.ownshelfDir[t].equals("E")) {
                shelfPick[t] = (ds.ownshelfX[t] + 30) / 30 + (ds.ownshelfY[t] / 30) * gridsizeX;
            }
            if (ds.ownshelfDir[t].equals("W")) {
                shelfPick[t] = (ds.ownshelfX[t] - 30) / 30 + (ds.ownshelfY[t] / 30) * gridsizeX;
            }

        }

        // Gör om x och y koordinater för shelves till nodnummer
        int[] shelfNodes = new int[ds.noShelves];

        for (int n = 0; n < ds.noShelves; n++) {
            shelfNodes[n] = ds.shelfX[n] / 30 + (ds.shelfY[n] / 30) * gridsizeX;
        }

        // Vår kod
        int[] obsNodes = new int[100];
        for (int n = 0; n < 100; n++) {
            obsNodes[n] = -1;
        }
        for (int n = 0; n < ds.noObstacles; n++) {
            obsNodes[n] = ds.obsX[n] / 30 + (ds.obsY[n] / 30) * gridsizeX;
        }

        int arc = 1;
        int arcCost_right = 1;
        int arcCost_top = 1;

        for (int i = 0; i <= gridsizeY - 2; i++) {
            for (int j = 0; j < gridsizeX - 1; j++) {
                if (contains(obsNodes, i * gridsizeX + j + 1) || contains(obsNodes, i * gridsizeX + j) || contains(shelfNodes, i * gridsizeX + j + 1) || contains(shelfNodes, i * gridsizeX + j)) {
                    arcCost_right = 1000;
                } else {
                    arcCost_right = 1;
                }
                if (contains(obsNodes, (i + 1) * gridsizeX + j) || contains(obsNodes, i * gridsizeX + j) || contains(shelfNodes, (i + 1) * gridsizeX + j) || contains(shelfNodes, i * gridsizeX + j)) {
                    arcCost_top = 1000;
                } else {
                    arcCost_top = 1;
                }

                Edge laneForward1 = new Edge("" + arc, nodes.get(i * gridsizeX + j),
                        nodes.get(i * gridsizeX + j + 1), arcCost_right); // Last argument is arc cost

                Edge laneForward2 = new Edge("" + arc + 1, nodes.get(i * gridsizeX + j),
                        nodes.get((i + 1) * gridsizeX + j), arcCost_top); // Last argument is arc cost

                Edge laneBackward1 = new Edge("" + arc + 2, nodes.get(i * gridsizeX + j + 1),
                        nodes.get(i * gridsizeX + j), arcCost_right); // Last argument is arc cost

                Edge laneBackward2 = new Edge("" + arc + 3, nodes.get((i + 1) * gridsizeX + j),
                        nodes.get((i) * gridsizeX + j), arcCost_top); // Last argument is arc cost

                arc = arc + 4;

                edges.add(laneForward1);
                edges.add(laneForward2);
                edges.add(laneBackward1);
                edges.add(laneBackward2);
            }
        }

        // Här genereras alla nodkombinationer med start och slutnod i definierade noder.
        List<List<Integer>> combinations = generateCombinations(shelfPick);

        for (int t = 0; t < combinations.size(); t++) {
            int start = ds.newStart;
            int end = 88;
            combinations.get(t).add(0, start);
            combinations.get(t).add(end);
            combinations.get(t).add(start);
        }

        // Här initieras djikstras graf / nodnät
        Graph graph = new Graph(nodes, edges);
        DijkstraAlgorithm dijkstra = new DijkstraAlgorithm(graph);

        int[] allTest = new int[1000]; // måste vara större än shelfpick
        int temp = 0;
        int currentBest = 100;
        int bestSlot = 0;
        int currentWorst = 1;
        int worstSlot = 0;

        for (int j = 0; j < combinations.size(); j++) {
            int startNode = combinations.get(j).get(0);
            dijkstra.execute(nodes.get(startNode));

            for (int i = 0; i < ds.ownnoShelves + 1; i++) {
                int nextShelf = combinations.get(j).get(i + 1);
                LinkedList<Vertex> path = dijkstra.getPath(nodes.get(nextShelf));
                allPaths[i] = path;
                temp = temp + path.size();

                dijkstra.execute(nodes.get(nextShelf));
            }
            allTest[j] = temp;
            if (temp < currentBest) {
                currentBest = temp;
                bestSlot = j;
            }

            if (temp > currentWorst) {
                currentWorst = temp;
                worstSlot = j;
            }
            temp = 0;
        }
        String[] turnComb = new String[ds.noObstacles];
        for (int q = 1; q < combinations.get(bestSlot).size() - 2; q++) {
//            System.out.println("test");
            for (int z = 0; z < ds.ownnoShelves; z++) {
//                System.out.println("shelfnode" + shelfPick[z]);
                if (combinations.get(bestSlot).get(q).equals(shelfPick[z])) {
//                    System.out.println("test3");
                    turnComb[q - 1] = ds.ownshelfDir[z];
//                    System.out.println("Turns: " + turnComb[q - 1]);
                }
            }
        }

//            System.out.println("Best slot " + bestSlot);
//            System.out.println("Best value " + currentBest);
//            System.out.println(combinations.get(bestSlot));
        for (int i = 0; i < combinations.get(bestSlot).size(); i++) {
            ds.routePlan = ds.routePlan + " " + Integer.toString(combinations.get(bestSlot).get(i) + 1);

        }

//        System.out.println("DS routeplan " + ds.routePlan);
//        String[] Plansplit = combinations.split(" ");
//            System.out.println("Worst slot " + worstSlot);
//            System.out.println("Worst value " + currentWorst);
//            System.out.println(combinations.get(worstSlot));
        int startNode = combinations.get(bestSlot).get(0);
        dijkstra.execute(nodes.get(startNode));

        int t = 0;

        for (int i = 0; i < ds.ownnoShelves + 1; i++) {
            int currentShelf = combinations.get(bestSlot).get(i);
            int nextShelf = combinations.get(bestSlot).get(i + 1);
//                System.out.println("NEXT SHELF " + nextShelf);
            LinkedList<Vertex> path = dijkstra.getPath(nodes.get(nextShelf));
            allPaths[i] = path;
//                System.out.println("All PATHS," + allPaths[i]);

            dijkstra.execute(nodes.get(nextShelf));

//            System.out.println("Shortest path from node " + currentShelf + " to node " + nextShelf);
            ds.pathLength = path.size();

            String Xformat = "";
            String Yformat = "";

            for (int j = 0; j < path.size() - 1; j++) {
                ds.linkStarts[t] = Integer.parseInt(path.get(j).getId());
                ds.linkEnds[t] = Integer.parseInt(path.get(j + 1).getId());
//                System.out.println(ds.linkStarts[t] + " " + ds.linkEnds[t]);
                ds.routeNodes = ds.routeNodes + ds.linkStarts[t] + "\n";
                ds.routeCoordinates = ds.routeCoordinates + ds.nodeX[ds.linkStarts[t]] + " "
                        + ds.nodeY[ds.linkStarts[t]] + ", "
                        + ds.nodeX[ds.linkEnds[t]] + " " + ds.nodeY[ds.linkEnds[t]] + "\n";

                if (t > 0) {
                    String direction = "";
                    if (ds.linkStarts[t] - 1 == currentShelf) {
//                        System.out.println("Här är currentshelf" + currentShelf);
                        for (int k = 0; k < combinations.get(bestSlot).size() - 3; k++) {
//                            System.out.println("Vår nod: " + (ds.linkStarts[t]-1) // la till -1
//                                    + " Routeplans nod: "
//                                    + combinations.get(bestSlot).get(k));
                            String noden = Integer.toString(ds.linkStarts[t] - 1); // la till -1
                            if (noden.equals(combinations.get(bestSlot).get(k + 1).toString())) {
//                                System.out.println("Vi är vid en hylla");
                                // Lägger till plockriktning i plocklistan
                                if (turnComb[k].equals("N")) {
                                    direction = "PS";
//                                    System.out.println(direction);
                                } else if (turnComb[k].equals("S")) {
                                    direction = "PN";
//                                    System.out.println(direction);
                                } else if (turnComb[k].equals("W")) {
                                    direction = "PE";
//                                    System.out.println(direction);
                                } else if (turnComb[k].equals("E")) {
                                    direction = "PW";
//                                    System.out.println(direction);
                                }
                                break;
                            }

                        }
                        if (ds.nodeX[ds.linkStarts[t] - 1] < 100) {
                            Xformat = "0" + ds.nodeX[ds.linkStarts[t] - 1];

                            if (ds.nodeX[ds.linkStarts[t] - 1] < 10) {
                                Xformat = "00" + ds.nodeX[ds.linkStarts[t] - 1];
                            }
                        } else {
                            Xformat = Integer.toString(ds.nodeX[ds.linkStarts[t] - 1]);
                        }
                        // skriver om koordinat till rätt format med nollor
                        if (ds.nodeY[ds.linkStarts[t] - 1] < 100) {
                            Yformat = "0" + ds.nodeY[ds.linkStarts[t] - 1];
                            // skriver om koordinat till rätt format med nollor

                            if (ds.nodeY[ds.linkStarts[t] - 1] < 10) {
                                Yformat = "00" + ds.nodeY[ds.linkStarts[t] - 1];
                            }
                        } else {
                            Yformat = Integer.toString(ds.nodeY[ds.linkStarts[t] - 1]);
                        }
                        String braFormat = Xformat + Yformat;

//                        ds.routeCom = ds.routeCom + braFormat + "_" ;
                        ds.routeCom = ds.routeCom + braFormat + "_" + direction + "_";
                        //kollar om det är en sväng
                    } else if (ds.nodeY[ds.linkStarts[t - 1] - 1] != ds.nodeY[ds.linkEnds[t] - 1]
                            && ds.nodeX[ds.linkStarts[t - 1] - 1] != ds.nodeX[ds.linkEnds[t] - 1]) {

                        // skriver om koordinat till rätt format med nollor
                        if (ds.nodeX[ds.linkStarts[t] - 1] < 100) { // m ändrar från t-1 till (t)-1
                            Xformat = "0" + ds.nodeX[ds.linkStarts[t] - 1]; // m ändrar

                            if (ds.nodeX[ds.linkStarts[t] - 1] < 10) {
                                Xformat = "00" + ds.nodeX[ds.linkStarts[t] - 1];
                            }
                        } else {
                            Xformat = Integer.toString(ds.nodeX[ds.linkStarts[t] - 1]);
                        }
                        // skriver om koodrdinat till rätt format med nollor
                        if (ds.nodeY[ds.linkStarts[t] - 1] < 100) { // matilda testar m -1
                            Yformat = "0" + ds.nodeY[ds.linkStarts[t] - 1]; // matilda testar m -1
                            if (ds.nodeY[ds.linkStarts[t] - 1] < 10) {
                                Yformat = "00" + ds.nodeY[ds.linkStarts[t] - 1];
                            }
                        } else {
                            Yformat = Integer.toString(ds.nodeY[ds.linkStarts[t] - 1]);
                        }

                        String braFormat = Xformat + Yformat;
                        ds.routeCom = ds.routeCom + braFormat + "_";
                    }
                }
                t = t + 1;
            }
        }

        // genererar bluetoothsträng
        ds.routeNodes = ds.routeNodes + ds.linkEnds[t]; // ändrar från t-1 till t
        ds.pathLength = currentBest;
//           System.out.println("DS nodePlan " + ds.routeNodes);
//        System.out.println("Hela plocklistan \n" + ds.routeCom);
//        System.out.println("Hela plocklistan \n" + shelfNodes[1] + " " + shelfNodes[2]);

    }

}
