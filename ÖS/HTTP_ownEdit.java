/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.kandidatprojektv2;

import java.io.*;
import java.net.*;
import java.sql.Timestamp;

public class HTTP_ownEdit implements Runnable {

    private int sleepTime;
    private DataStore ds;
    private ControlUI cui;

    public HTTP_ownEdit(DataStore ds) {
        this.ds = ds;
        sleepTime = 15000;
    }

    public String getTimeStamp() {
        Timestamp timestamp = new Timestamp(System.currentTimeMillis());
        String[] se = timestamp.toString().split(" ");
        String[] h = se[1].split("\\.");
        String onlyTime = h[0];
        return onlyTime;
    }

    @Override
    public void run() {
        int counter = 0;
        int test = 0;
        int wishListNo = 0;
        int u = 0;
        boolean hasStopped = false;
        while(counter != 900) {
        try {

            
           // while (test != 900) {
                // Meddelande fån Amanda & Fanny:
                // Catchen fångar upp tråden efter 10-13 körningar av while-loopen
                // Det vi vill att den ska göra är ju att tråden ska somna antingen efter 2 min
                // , men den stannar nu efter ish en halv minut
                // Är man snabb på att trycka på start efter det att alla hyllor är tagna
                // funkar koden.. men det känns ju inte så bra

                // Kollisionskontrollen funkar, men skrivs inte ut i rätt tuta i GUIn
                Thread.sleep(1000);
                if (ds.httpStart == true) {
                    u++;
//                    String urlTasks = "https://n7.se/listtasks.php";
//                    URL n7List = new URL("https://n7.se/listtasks.php");
//                    URL assign_n7 = new URL("https://n7.se/assigntasks.php?id=1&t=3");
                    String urlClaim = "https://n7.se/assigntasks.php?id=";
//                    URL urlobjekt = new URL(urlTasks);
//                    URL urlobjektClaim = new URL(urlClaim);
                    String AGVpos = "https://n7.se/pos.php?id=";
//                    URL urlobjectPos = new URL(AGVpos);
                    if (ds.beginPos == false) {
                        if (u == 10) { // tar alla hyllor efter 10s
                            wishListNo = 0;
                            ds.wishList = ds.allList;
                        }
                        if (ds.wishList[wishListNo] == 0) { // börjar om på listan om vi gått för långt
                            wishListNo = 0;
                        }

                        String claimShelfs = urlClaim + ds.id + "&t=" + ds.wishList[wishListNo];
                        wishListNo = wishListNo + 1;
                        URL urlTest = new URL(claimShelfs);
                        System.out.println(claimShelfs);
                        HttpURLConnection nSeven = (HttpURLConnection) urlTest.openConnection();

                        BufferedReader in = new BufferedReader(new InputStreamReader(nSeven.getInputStream()));   //(nSeven.openStream));
                        String inputLine;
                        while ((inputLine = in.readLine()) != null) {
                            System.out.println(inputLine);
                        }
                        in.close();
                    } //while börjar om

                    if (ds.beginPos == true) {
                        //"https://n7.se/pos.php?id=1&x=30&y=60" - position
                        String sendPos = AGVpos + ds.id + "&x=" + ds.xAGV + "&y=" + ds.yAGV;
                        URL sendingPos = new URL(sendPos);
                        HttpURLConnection checkPos = (HttpURLConnection) sendingPos.openConnection();

                        BufferedReader inn = new BufferedReader(new InputStreamReader(checkPos.getInputStream()));   //(nSeven.openStream));
                        String inputLinee;

                        if ((inputLinee = inn.readLine()) != null) {
                            String[] splitInput = inputLinee.split(",");
                            ds.xOtherAGV = splitInput[1];
                            ds.yOtherAGV = splitInput[2];
                            ds.otherPos = "Annan AGV X: " + ds.xOtherAGV + " Y: " + ds.yOtherAGV + "\n";

                            //kollision-kontroll
                            int ay = Integer.parseInt(ds.yOtherAGV);
                            int ax = Integer.parseInt(ds.xOtherAGV);
                            double x = Integer.parseInt(ds.xAGV) - ax;
                            double y = Integer.parseInt(ds.yAGV) - ay;

                            double hypot = Math.hypot(x, y);
                            if (hypot < 90 || (ax <= 30 && ay <= 150 && ay >= 90)) {
                                if (hasStopped == false) {
                                    System.out.println("PANG");
                                    ds.command = getTimeStamp() + "_S"; //kan ej skicka till agv?
                                    System.out.println("PANG2");
                                    hasStopped = true;
                                    System.out.println("Bytt till true");
                                }
                            } else if (hasStopped == true) {
                                hasStopped = false;
                                System.out.println("Bytt till false");

                            }

                        }
                        inn.close();
                    }
                    
                }
                test++;
                counter++;
            //}
        } catch (Exception ee) {
            System.out.println("connection failed ++++++++++++++++++++++++++ \n");
        }
        }
    }

}
