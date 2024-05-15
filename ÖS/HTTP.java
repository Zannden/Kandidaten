/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.kandidatprojektv2;

import java.io.*;
import java.net.*;

//FUNKTION: skriver ut och kollar listan
public class HTTP implements Runnable {

    private int sleepTime;
    private DataStore ds;

    public HTTP(DataStore ds) {
        this.ds = ds;
        sleepTime = 15000; //orig 20000
    }

    @Override
    public void run() {
        try {
//            HTTPanrop http = new HTTPanrop();
            // https://n7.se/inittasks.php?num=A - initiera antal hyllor, ska ske manuellt innan ruttplan
            // https://n7.se/listtasks.php - lista hyllor, vilka som finns kvar/är tagna
            // https://n7.se/assigntasks.php?id=1&t=3 - assigna vilken hylla respektive ID tar
            //"https://n7.se/pos.php?id=1&x=30&y=60" - position

            String urlTasks = "https://n7.se/listtasks.php";
            //String urlClaim = "https://n7.se/assigntasks.php?id=";
            URL urlobjekt = new URL(urlTasks);
            //URL urlobjektClaim = new URL(urlClaim);

            int test = 0;

            while (test != 900 && ds.beginPos == false) {
                Thread.sleep(500);

                if (ds.httpStart == true && ds.beginPos == false) {

                    // öppnar listan över uppdrag och visar om anslutning lyckades
                    // status 200 innebär att HTTP har förstått
                    HttpURLConnection anslutningTasks = (HttpURLConnection) urlobjekt.openConnection();
                    System.out.println("\nAnropar: " + urlTasks);

                    int mottagen_status = anslutningTasks.getResponseCode();
                    System.out.println("Statuskod: " + mottagen_status);

                    // läser av texten som fås från anslutningen
                    BufferedReader inkommande = new BufferedReader(new InputStreamReader(anslutningTasks.getInputStream()));
                    String inkommande_text;
                    String allaUppdrag = "";
//            allaUppdrag.length() < 30;

                    StringBuffer inkommande_samlat = new StringBuffer();
                    int count = 0;
                    int temp = 0;

                    while ((inkommande_text = inkommande.readLine()) != null) {
                        inkommande_samlat.append(inkommande_text);
                        ds.allTasks[count] = inkommande_text;
                        count = count + 1;
                        allaUppdrag = allaUppdrag + inkommande_text + "  ";
                    }

                    inkommande.close();
                    ds.allTasksList = allaUppdrag;

                    String[] splittad = allaUppdrag.split(",");
                    ds.ownnoShelves = 0;
                    for (int i = 0; i <= splittad.length - 3; i = i + 2) {
                        int hyllnr = Integer.parseInt(splittad[i].strip());
                        int AGVnr = Integer.parseInt(splittad[i + 1]);
                        System.out.println(splittad.length);
                        if (AGVnr == ds.id) {
                            ds.ownshelfDir[temp] = ds.shelfDir[hyllnr - 1];
                            ds.ownshelfX[temp] = ds.shelfX[hyllnr - 1];
                            ds.ownshelfY[temp] = ds.shelfY[hyllnr - 1];

                            ds.ownnoShelves = ds.ownnoShelves + 1;
                            System.out.println("Hyllnr " + hyllnr + "Dir: " + ds.ownshelfDir[temp] + " X " + ds.ownshelfX[temp] + " Y " + ds.ownshelfY[temp] + " Totantal " + ds.ownnoShelves);
                            temp = temp + 1;
                        }
                    }

                    allaUppdrag = "";

//                    Thread.sleep(sleepTime / 8);
                }
                test++;
            }

        } catch (Exception e) {
            System.out.print(e.toString());
        }

    }

}



