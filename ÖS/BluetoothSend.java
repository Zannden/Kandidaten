/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.kandidatprojektv2;

import java.io.*;
import javax.microedition.io.*;
import javax.bluetooth.*;
import java.sql.Timestamp;


public class BluetoothSend implements Runnable {

    private int sleepTime;
    private DataStore ds;
    private static String nodes;

    public BluetoothSend(DataStore ds) {
        this.ds = ds;
        sleepTime = 15000;
        nodes = ds.routeNodes;
    }

    @Override
    public void run() {
        try {
            PrintStream bluetooth_out = new PrintStream(ds.connection.openOutputStream());
            BufferedReader keyboard = new BufferedReader(new InputStreamReader(System.in));

            // Thread.sleep(sleepTime / 20);
            String message_out = ds.command;

            while (true) {
                // System.out.println("hej");
                Thread.sleep(sleepTime / 20);
                //tangentbord.readLine();
                if (!message_out.equals(ds.command)) {
                    message_out = ds.command;

                    bluetooth_out.println(message_out);
                    if (message_out == null) {
                        break;
                    }
                }

            }

            // if-loop: vårt id = 1. Läs kontinuerligt av hemsidan för den andra AGVn
            // jämför våra koordinater med den andra AGVns. beräkna skillnad mellan X och Y
            // 
            ds.connection.close();
            bluetooth_out.close();
            keyboard.close();
        } catch (Exception e) {
            System.out.print(e.toString());
            System.out.println("fail");
        }
    }
}

// try { 
//            cui.appendStatus("\n\nTruckRead kommer att vänta i " + sleepTime + " millisekunder.\n");
//            int i = 1; 
//            while (i <= 20) {
//                Thread.sleep(sleepTime / 20);
//                cui.appendStatus("Tråd TruckRead för "+i+":te gången.\n"); 
//                if(i == 10){ 
//                    ds.updateUIflag = true; 
//                }
//                i++; 
//            } 
//        } 
//        catch (InterruptedException exception) {
//        }
//        cui.appendStatus("TruckRead är nu klar!\n"); 
//    } 
