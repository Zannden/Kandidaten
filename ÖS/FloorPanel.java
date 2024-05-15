/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/GUIForms/JPanel.java to edit this template
 */
package com.mycompany.kandidatprojektv2;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;

/**
 *
 * @author clary35
 */
public class FloorPanel extends javax.swing.JPanel {

    DataStore ds;

    /**
     * Creates new form FloorPanel
     */
    public FloorPanel(DataStore ds) {
        this.ds = ds;
        initComponents();
    }

    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        final Color LIGHT_COLOR = new Color(150, 150, 150);
        final Color DARK_COLOR = new Color(0, 0, 0);
        final Color RED_COLOR = new Color(255, 0, 0);
        final Color GREEN_COLOR = new Color(0, 204, 0);
        final Color LIGHTBLUE_COLOR = new Color(51, 204, 255);
        final Color DARKBLUE_COLOR = new Color(0, 0, 153);

        int panelHeight = getHeight();
        int panelWidth = getWidth();

        double xscale = 1.0 * panelWidth / 690.0;
        double yscale = 1.0 * panelHeight / 300.0;

        int gridsizeX = 21;
        int gridsizeY = 9;
        int offsetX = 60;
        int offsetY = 30;
        int distX = 30;
        int distY = 30;
        int nodeSize = 5;
        int obsSize = 20;
        int dirSize = 10;

        if (ds.layoutRead == true) {
            // Draw nodes
            for (int x = 0; x < gridsizeX; x++) {
                for (int y = 0; y < gridsizeY; y++) {
                    g.fillOval((int) (offsetX * xscale + x * distX * xscale - nodeSize / 2),
                            (int) (offsetY * yscale + y * distY * yscale - nodeSize / 2), nodeSize, nodeSize);
                }
            }
            Graphics2D g2 = (Graphics2D) g;
            // Draw horizontal arcs
            for (int x = 0; x < gridsizeX - 1; x++) {
                for (int y = 0; y < gridsizeY; y++) {
                    g2.setStroke(new BasicStroke(1));
                    g.setColor(DARK_COLOR);
                    for (int i = 0; i < ds.pathLength; i++) {
                        if ((y * (gridsizeX + 1) + x == ds.linkStarts[i] - 1 && y * (gridsizeX + 1) + x + 1 == ds.linkEnds[i] - 1) || (y * (gridsizeX + 1) + x + 1 == ds.linkEnds[i] - 1 && y * (gridsizeX + 1) + x == ds.linkStarts[i] - 1)) {
                            g2.setStroke(new BasicStroke(3));
                            g.setColor(RED_COLOR);
                        }
                        if ((y * (gridsizeX + 1) + x == ds.linkEnds[i] - 1 && y * (gridsizeX + 1) + x + 1 == ds.linkStarts[i] - 1) || (y * (gridsizeX + 1) + x + 1 == ds.linkStarts[i] - 1 && y * (gridsizeX + 1) + x == ds.linkEnds[i] - 1)) {
                            g2.setStroke(new BasicStroke(3));
                            g.setColor(RED_COLOR);
                        }
                    }
                    g.drawLine((int) (xscale * (offsetX + x * distX)), panelHeight - (int) (yscale * (offsetY + y * distY)), (int) (xscale * (offsetX + (x + 1) * distX)), panelHeight - (int) (yscale * (offsetY + y * distY)));
                }
            }
            // Draw vertical arcs
            for (int x = 0; x < gridsizeX; x++) {
                for (int y = 0; y < gridsizeY - 1; y++) {
                    g2.setStroke(new BasicStroke(1));
                    g.setColor(DARK_COLOR);
                    for (int i = 0; i < ds.pathLength; i++) {
                        if ((y * (gridsizeX + 1) + x == ds.linkStarts[i] - 1 && (y + 1) * (gridsizeX + 1) + x == ds.linkEnds[i] - 1) || ((y + 1) * (gridsizeX + 1) + x == ds.linkStarts[i] - 1 && y * (gridsizeX + 1) + x == ds.linkEnds[i] - 1)) {
                            g2.setStroke(new BasicStroke(3));
                            g.setColor(RED_COLOR);

                        }
                    }
                    g.drawLine((int) (xscale * (offsetX + x * distX)), panelHeight - (int) (yscale * (offsetY + y * distY)), (int) (xscale * (offsetX + x * distX)), panelHeight - (int) (yscale * (offsetY + (y + 1) * distY)));
                }
            }
            // Draw obstacles
            g.setColor(RED_COLOR);
            for (int k = 0; k < ds.noObstacles; k++) {
                g.fillOval((int) (offsetX * xscale + ds.obsX[k] * xscale - obsSize / 2),
                        panelHeight - (int) (offsetY * yscale + ds.obsY[k] * yscale + obsSize / 2), obsSize, obsSize);
            }
            // Draw Shelves 
            g.setColor(GREEN_COLOR);
            for (int k = 0; k < ds.noShelves; k++) {
                int posX = (int) (offsetX * xscale + ds.shelfX[k] * xscale - obsSize / 2);
                int posY = panelHeight - (int) (offsetY * yscale + ds.shelfY[k] * yscale + obsSize / 2);
                g.fillOval(posX, posY, obsSize, obsSize);

                //Draw Directions
                if (ds.shelfDir[k].equals("S")) {
                    g.fillOval(posX + 5, posY + 20, dirSize, dirSize);
                }
                if (ds.shelfDir[k].equals("N")) {
                    g.fillOval(posX + 5, posY - 10, dirSize, dirSize);
                }
                if (ds.shelfDir[k].equals("W")) {
                    g.fillOval(posX - 10, posY + 5, dirSize, dirSize);
                }
                if (ds.shelfDir[k].equals("E")) {
                    g.fillOval(posX + 20, posY + 5, dirSize, dirSize);
                }
            }
            //Draw Finish
            g.setColor(DARKBLUE_COLOR);
            g.fillRect((int) (offsetX * xscale - 30 * xscale - obsSize / 2),
                    panelHeight - (int) (offsetY * yscale + 120 * yscale + obsSize / 2), obsSize, obsSize);
            //LÄGG TILL EN EXTRA BÅGE? 
//           g.drawLine((int) (xscale * (offsetX -30 * distX)), panelHeight - (int) (yscale * (offsetY + 120 * distY)), (int) (xscale * (offsetX + (0 + 1) * distX)), panelHeight - (int) (yscale * (offsetY + 120 * distY)));

            //Draw Start
            g.setColor(LIGHTBLUE_COLOR);
            g.fillRect((int) (offsetX * xscale + 0 * xscale - obsSize / 2),
                    panelHeight - (int) (offsetY * yscale + 60 * yscale + obsSize / 2), obsSize, obsSize);
            g.fillRect((int) (offsetX * xscale + 0 * xscale - obsSize / 2),
                    panelHeight - (int) (offsetY * yscale + 180 * yscale + obsSize / 2), obsSize, obsSize);

            //Draw own truck
            g.setColor(DARK_COLOR);
            int truckSize = 30;
            g.drawOval((int) (offsetX * xscale + Integer.parseInt(ds.xAGV) * xscale - truckSize / 2), panelHeight - (int) (offsetY * yscale + Integer.parseInt(ds.yAGV) * yscale + truckSize / 2), truckSize, truckSize);

            //Draw other truck
            g.setColor(RED_COLOR);
            g.drawOval((int) (offsetX * xscale + Integer.parseInt(ds.xOtherAGV) * xscale - truckSize / 2), panelHeight - (int) (offsetY * yscale + Integer.parseInt(ds.yOtherAGV) * yscale + truckSize / 2), truckSize, truckSize);

        }

    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor. if (ds.problemRead == true) { *
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 400, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 300, Short.MAX_VALUE)
        );
    }// </editor-fold>//GEN-END:initComponents


    // Variables declaration - do not modify//GEN-BEGIN:variables
    // End of variables declaration//GEN-END:variables
}
