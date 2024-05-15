/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.kandidatprojektv2;

/**
 * * * @author clary35
 */
public class GuiUpdate implements Runnable {

    private int sleepTime;
    private ControlUI cui;
    private DataStore ds;

    public GuiUpdate(DataStore ds, ControlUI cui) {
        this.cui = cui;
        this.ds = ds;
        sleepTime = 8000; //orig 15000
    }

    @Override
    public void run() {
        int count = 0;
        while (count != 900) {
        try {

            int test = 0;

            //while (test != 120) {

                if (ds.beginPos == true) {
                    cui.appendHTTPpos(ds.otherPos);
                } else {
                    cui.appendHTTP(ds.allTasksList);
                }

                cui.appendAGVStatus(ds.AGVStatus);

                cui.repaint();

                Thread.sleep(1000);
                test++;

            //}

            Thread.sleep(500);
            count++;

        } catch (InterruptedException exception) {
        }
        }
        //cui.appendStatus("GuiUpdate är nu klar!\n"); 
    }
}
