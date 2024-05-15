/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.kandidatprojektv2;

/**
 *
 * @author itn
 */
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
public class HTTPanrop {
    private static DataStore ds;
        

    public static void main(String[] args) {
        try {
            HTTPanrop http = new HTTPanrop();
            // https://n7.se/inittasks.php?num=A - initiera antal hyllor, ska ske manuellt innan ruttplan
            //https://n7.se/listtasks.php - lista hyllor, vilka som finns kvar/är tagna
            //https://n7.se/assigntasks.php?id=1&t=3 - assigna vilken hylla respektive ID tar
            //"https://n7.se/pos.php?id=1&x=30&y=60" - position
            String urlTasks = "https://n7.se/listtasks.php";
            String urlClaim = "https://n7.se/assigntasks.php";
            URL urlobjekt = new URL(urlTasks);
            HttpURLConnection anslutning = (HttpURLConnection) urlobjekt.openConnection();
            System.out.println("\nAnropar: " + urlTasks);
            int mottagen_status = anslutning.getResponseCode();
            System.out.println("Statuskod: " + mottagen_status);
            BufferedReader inkommande = new BufferedReader(new InputStreamReader(anslutning.getInputStream()));
            String inkommande_text;
            String allaUppdrag = "";
            
            StringBuffer inkommande_samlat = new StringBuffer();
            
            
            while ((inkommande_text = inkommande.readLine()) != null) {
                inkommande_samlat.append(inkommande_text);
                allaUppdrag = allaUppdrag + inkommande_text;
                ds.allTasks[0] = (inkommande_text);
                
            }
            inkommande.close();
            System.out.println(inkommande_samlat.toString());
            System.out.println("All Tasks " + ds.allTasks[0]);
        } catch (Exception e) {
            System.out.print(e.toString());
        }
    }
}
