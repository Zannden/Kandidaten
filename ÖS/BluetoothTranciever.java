/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.kandidatprojektv2;
import java.io.*;
import javax.microedition.io.*;
import javax.bluetooth.*;

public class BluetoothTranciever {
    private DataStore ds;
    private static String nodes;
        
    public BluetoothTranciever(DataStore ds) {
        this.ds = ds;
        nodes = ds.routeNodes;
        
    }
    
    public static void main(String args[]) {
        
        try {
            StreamConnection anslutning = (StreamConnection) Connector.open("btspp://B827EB418F6D:1");
            PrintStream bluetooth_ut = new PrintStream(anslutning.openOutputStream());
            BufferedReader bluetooth_in = new BufferedReader(new InputStreamReader(anslutning.openInputStream()));
            BufferedReader tangentbord = new BufferedReader(new InputStreamReader(System.in));
            
            
            
            while (true) {
                    System.out.println("Stannar du här?");
                    String meddelande_ut = tangentbord.readLine();
                    System.out.println("Eller här?");
                    bluetooth_ut.println(meddelande_ut);
                    System.out.println("Kanske här?");
                    
                    if (meddelande_ut == null) {
                        break;
                    }
                    String meddelande_in = bluetooth_in.readLine();
                    System.out.println("AGV: " + meddelande_in);

            }
            
            anslutning.close();
            bluetooth_ut.close();
            bluetooth_in.close();
            tangentbord.close();
        } catch (Exception e) {
            System.out.print(e.toString());
            System.out.println("fail");
        }
    }
}
