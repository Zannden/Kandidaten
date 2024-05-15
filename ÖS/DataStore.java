/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.kandidatprojektv2;

import java.io.File;
import java.util.Scanner;
import javax.microedition.io.Connector;
import javax.microedition.io.StreamConnection;

public class DataStore {

    boolean layoutRead;
    boolean updateUIflag;
    public volatile boolean httpStart;
    boolean beginPos;
    String fileName = "/home/itn/NetBeansProjects/Kandidatprojektv2/src/main/java/com/mycompany/kandidatprojektv2/newLayout.txt";
    int noObstacles;
    int noShelves;
    int[] obsX;
    int[] obsY;
    int[] shelfX;
    int[] shelfY;
    int[] shelfPickX;
    int[] shelfPickY;
    String[] shelfDir;
    String infoText;
    String routePlan; //lista med alla noder vi VILL besöka, start-hyllor-slut
    String routeNodes; // varenda nod vi faktiskt passerar i den optimala rutten
    String routeCoordinates;
    String routeCom;
    String routeProtocol;
    String[] ownshelfDir;
    int[] ownshelfX;
    int[] ownshelfY;
    int ownnoShelves;

    String[] allTasks;
    String allTasksList;
    String assignURL;

    String AGVStatus;
    String command;
    int newStart;
    int id;
    String newStartCo;
    String nodText;
    String endKo;

    int[] nodeX;
    int[] nodeY;

    int pathLength;
    int[] linkStarts;
    int[] linkEnds;
    int startNode;
    int endNode;

    double truck1X;
    double truck1Y;

    double truck2X;
    double truck2Y;

    int[] wishList;
    int[] wishListPos2;
    int[] wishListPos1;
    int[] allList;
    String xAGV;
    String yAGV;
    String xOtherAGV;
    String yOtherAGV;
    String otherPos;

    StreamConnection connection;

    DataStore() {
        layoutRead = false;
        updateUIflag = false;
        httpStart = false;
        beginPos = false;
        obsX = new int[100];
        obsY = new int[100];
        shelfX = new int[100];
        shelfY = new int[100];
        shelfDir = new String[100];
        shelfPickX = new int[100];
        shelfPickY = new int[100];

        pathLength = 0;
        linkStarts = new int[1000];
        linkEnds = new int[1000];
        routePlan = "";
        routeNodes = "";
        routeCoordinates = "";
        routeCom = "";
        routeProtocol = "";

        allTasks = new String[100];
        allTasksList = "";
        assignURL = "";

        AGVStatus = "";
        command = "";
        newStart = 44;
        id = 2;
        newStartCo = "";
        nodText = "";
        endKo = "000120";

        truck1X = 0;
        truck1Y = 180;
        truck2X = 0;
        truck2Y = 60;
        nodeX = new int[220];
        nodeY = new int[220];
        startNode = 110;
        endNode = 140;

        xAGV = "000";
        yAGV = "060";
        xOtherAGV = "300";
        yOtherAGV = "300";
        otherPos = "\n";

        ownshelfDir = new String[100];
        ownshelfX = new int[100];
        ownshelfY = new int[100];
        ownnoShelves = 0;

    }

    public void readLayout() {
        String line;

        try {
            File file = new File(fileName);
            Scanner scanner = new Scanner(file, "UTF-8");
            String[] sline;

            // Read obstacle data
            line = (scanner.nextLine());
            noObstacles = Integer.parseInt(line.split(",")[0].trim());
            // System.out.println("Obstacles: " + noObstacles);
            infoText = "Obstacles: " + noObstacles + "\n"; //textruta

            for (int i = 0; i < noObstacles; i++) {
                line = (scanner.nextLine());
                obsX[i] = Integer.parseInt(line.split(",")[0].trim());
                obsY[i] = Integer.parseInt(line.split(",")[1].trim());
                // System.out.println("Obstacle " + i + ": x= " + obsX[i] + " y= " + obsY[i]);
                infoText = infoText + "Obstacle " + i + ": x=" + obsX[i] + " y= " + obsY[i] + "\n";
            }
            // Read shelf data
            line = (scanner.nextLine());
            noShelves = Integer.parseInt(line.split(",")[0].trim());
//            System.out.println("Shelves: " + noShelves); 
            infoText = infoText + "Shelves: " + noShelves + "\n";//textruta

            wishListPos2 = new int[noShelves];
            wishListPos1 = new int[noShelves];
            wishList = new int[noShelves];
            allList = new int[noShelves];

            int pos1 = 0;
            int pos2 = 0;
            for (int i = 0; i < noShelves; i++) {
                line = (scanner.nextLine());
                shelfX[i] = Integer.parseInt(line.split(",")[0].trim());
                shelfY[i] = Integer.parseInt(line.split(",")[1].trim());
                shelfDir[i] = line.split(",")[2].trim();
//                System.out.println("Shelf " + i + ": x= " + shelfX[i] + " y= " + shelfY[i] + " Dir= " + shelfDir[i]);
                infoText = infoText + "Shelf " + i + ": x= " + shelfX[i] + " y= " + shelfY[i] + " Dir= " + shelfDir[i] + "\n";
                allList[i] = i + 1;

                if (shelfY[i] > 120) {
                    wishListPos1[pos2] = i + 1;
                    pos2++;
                }
                if (shelfY[i] <= 120) {
                    wishListPos2[pos1] = i + 1;
                    pos1++;
                }
            }

            // Indicate that all data is read
            layoutRead = true;
            connection = (StreamConnection) Connector.open("btspp://B827EB418F6D:1");

        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

    }

    public class TextProvider {

        public static String getText() {
            return "testing";
        }
    }

}
