/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */
package com.mycompany.kandidatprojektv2;

public class Kandidatprojektv2 {

    DataStore ds;
    ControlUI cui;

    Kandidatprojektv2() {
        // Initialize the DataStore 
        ds = new DataStore();

        // Load the obstacles and shelf locations
        ds.readLayout();

        // OptPlan op = new OptPlan(ds); 
        // op.createPlan();
        cui = new ControlUI(ds);
        cui.setVisible(true);

        //BluetoothTranciever bluetooth = new BluetoothTranciever(ds);
        //Thread t3 = new Thread(bluetooth);
        //Bluetooth tr1 = new Bluetooth(ds, cui); 
        BluetoothRecieve tr1 = new BluetoothRecieve(ds);
        Thread t1 = new Thread(tr1);

        BluetoothSend tr2 = new BluetoothSend(ds);
        Thread t2 = new Thread(tr2);

        HTTP tr3 = new HTTP(ds);
        Thread t3 = new Thread(tr3);

        GuiUpdate tr4 = new GuiUpdate(ds, cui);
        Thread t4 = new Thread(tr4);

        HTTP_ownEdit tr5 = new HTTP_ownEdit(ds);
        Thread t5 = new Thread(tr5);

        //System.out.println("Startar 2 trådar...");
        t1.start();
        t2.start();
        t3.start();
        t4.start();
        t5.start();
        //System.out.println("Trådar startade, main avslutas"); 

    }

    public static void main(String[] args) {
        Kandidatprojektv2 x = new Kandidatprojektv2();
    }
}
