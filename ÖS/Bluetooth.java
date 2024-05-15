/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.kandidatprojektv2;


import java.io.*;
import javax.microedition.io.*;
import javax.bluetooth.*;

public class Bluetooth implements Runnable{ 
    private int sleepTime; 
    private ControlUI cui; 
    private DataStore ds;
    private static String nodes;
    
    public Bluetooth(DataStore ds, ControlUI cui) {
        this.cui = cui; this.ds = ds; sleepTime = 15000;
        nodes = ds.routeNodes;
    }
    
    @Override 
    public void run() { 
                try {
            StreamConnection connection = (StreamConnection) Connector.open("btspp://B827EB418F6D:1");
            PrintStream bluetooth_out = new PrintStream(connection.openOutputStream());
            BufferedReader bluetooth_in = new BufferedReader(new InputStreamReader(connection.openInputStream()));
            BufferedReader keyboard = new BufferedReader(new InputStreamReader(System.in));
            Boolean sending = true;
            Boolean receive = false;
            Boolean close = false;
            Thread.sleep(sleepTime / 20);
            
            while (close == false) {
            
                while (sending == true) {
                    String message_out = keyboard.readLine();
                    bluetooth_out.println(message_out);
                    if (message_out.equals(";")) {
                        sending = false;
                        receive = true;
                    }
                    if (message_out.equals("STOP")) {close = true;}
                }
                
                if (close == true) {break;}
            
                while (receive == true) {
                    String message_in = bluetooth_in.readLine();
                    System.out.println("AGV: " + message_in);
                    if (message_in.equals(";")) {
                        sending = true;
                        receive = false;
                    }
                }
                
            }
            
            connection.close();
            bluetooth_out.close();
            bluetooth_in.close();
            keyboard.close();
        } catch (Exception e) {
            System.out.print(e.toString());
            System.out.println("fail");
        }
}
}