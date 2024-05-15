/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.kandidatprojektv2;

import java.io.*;
import javax.microedition.io.*;
import javax.bluetooth.*;


public class BluetoothRecieve implements Runnable {

    private int sleepTime;
    private DataStore ds;
    private static String nodes;

    public BluetoothRecieve(DataStore ds) {
        this.ds = ds;
        sleepTime = 15000;
        nodes = ds.routeNodes;
    }

    @Override
    public void run() {
        try {
            BufferedReader bluetooth_in = new BufferedReader(new InputStreamReader(ds.connection.openInputStream()));

            Thread.sleep(sleepTime / 20);
            String temp = "";

            while (true) {

                String message_in = bluetooth_in.readLine();

                if (!message_in.equals(temp)) {
                    ds.AGVStatus = message_in + "\n";
                    temp = message_in;

                }

                System.out.println("AGV: " + message_in);

                if (message_in == null) {
                    break;
                }

                // en if-sats som bara gör uppdelningen av AGVns koordinater
                // efter att start-knappen har tryckts
                int n = ds.command.length();
                char lastChar = ds.command.charAt(n - 1);
                char begin = 'B';

                if (lastChar == begin) {
                    String xyAGV;

                    //delar meddelandet efter "_"
                    String[] splittedMessage = message_in.split("_");

                    //sparar mittenpartiet i en egen sträng
                    xyAGV = splittedMessage[1];

                    //delar koordinater i två och sparar dem i två separata strängar
                    int mid = xyAGV.length() / 2;
                    String[] parts = {xyAGV.substring(0, mid), xyAGV.substring(mid)};
                    ds.xAGV = parts[0];
                    ds.yAGV = parts[1];

                }
            }

            ds.connection.close();
            bluetooth_in.close();

        } catch (Exception e) {
            System.out.print(e.toString());
            System.out.println("fail");
        }
    }
}
