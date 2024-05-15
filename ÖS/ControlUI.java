/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/GUIForms/JFrame.java to edit this template
 */
package com.mycompany.kandidatprojektv2;

import java.sql.Timestamp;
//import java.util.Date;

public class ControlUI extends javax.swing.JFrame {

    DataStore ds;

    /**
     * Creates new form ControlUI
     */
    public ControlUI() {
        initComponents();
    }

    public ControlUI(DataStore ds) {
        this.ds = ds;
        initMyComponents();
    }

    public void appendStatus(String text) {
        AGVruta.append(text);
        AGVruta.setCaretPosition(AGVruta.getDocument().getLength());
    }

    // Här har Joakim adderat 
    public void appendHTTP(String text) {
        HTTPruta.setText("");
        HTTPruta.append(text);
        HTTPruta.setCaretPosition(HTTPruta.getDocument().getLength());
    }

    public void appendHTTPpos(String text) {
        String[] temp = HTTPruta.getText().split("\n");
        if (!(temp[temp.length - 1] + "\n").equals(ds.otherPos)) {
            HTTPruta.append(text);
            HTTPruta.setCaretPosition(HTTPruta.getDocument().getLength());
        }
    }

    public void appendAGVStatus(String text) {
        String[] temp = AGVruta.getText().split("\n");
        if (!(temp[temp.length - 1] + "\n").equals(ds.AGVStatus)) {
            AGVruta.append(text);
            AGVruta.setCaretPosition(AGVruta.getDocument().getLength());
        }
    }

    public String getTimeStamp() {
        Timestamp timestamp = new Timestamp(System.currentTimeMillis());
        String[] se = timestamp.toString().split(" ");
        String[] h = se[1].split("\\.");
        String onlyTime = h[0];
        return onlyTime;
    }

    public void newInfo() {
        ds.nodText = nyStartRuta.getText();
        String[] splittad = ds.nodText.split(",");
        ds.newStart = Integer.parseInt(splittad[0]);
        ds.newStartCo = splittad[1];
        ds.routeCom = "";
        if (splittad.length > 2) {
            if (splittad[2].equals("h")) {
                int mid = splittad[3].length() / 2;
                String[] parts = {splittad[3].substring(0, mid), splittad[3].substring(mid)};
                ds.obsX[ds.noObstacles] = Integer.parseInt(parts[0]);
                ds.obsY[ds.noObstacles] = Integer.parseInt(parts[1]);
                RUTTruta.append(" Hinder tillagt vid " + ds.obsX[ds.noObstacles] + "," + ds.obsY[ds.noObstacles]);
                ds.noObstacles = ds.noObstacles + 1;

            }
        }
        RUTTruta.append("\n Du skrev: " + ds.newStart + " OCH " + ds.newStartCo + "\n");
        nyStartRuta.setText("");
    }
    // Här slutar Joakims input

    private void initMyComponents() {

        jPanel1 = new FloorPanel(ds); //VIKTIG att ej copypastea över!
        StartKnapp = new javax.swing.JButton();
        ScrollAGVruta = new javax.swing.JScrollPane();
        AGVruta = new javax.swing.JTextArea();
        ScrollHTTPruta = new javax.swing.JScrollPane();
        HTTPruta = new javax.swing.JTextArea();
        StoppKnapp = new javax.swing.JButton();
        CheckKnapp = new javax.swing.JButton();
        RuttKnapp = new javax.swing.JButton();
        nyStartRuta = new javax.swing.JTextField();
        pos2Knapp = new javax.swing.JButton();
        pos1Knapp = new javax.swing.JButton();
        ScrollRUTTruta = new javax.swing.JScrollPane();
        RUTTruta = new javax.swing.JTextArea();
        enterKnapp = new javax.swing.JButton();
        claimKnapp = new javax.swing.JButton();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        setExtendedState(6);

        jPanel1.setBackground(new java.awt.Color(255, 255, 255));

        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
                jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGap(0, 0, Short.MAX_VALUE)
        );
        jPanel1Layout.setVerticalGroup(
                jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGap(0, 274, Short.MAX_VALUE)
        );

        StartKnapp.setBackground(new java.awt.Color(0, 204, 0));
        StartKnapp.setText("START");
        StartKnapp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                StartKnappActionPerformed(evt);
            }
        });

        AGVruta.setColumns(20);
        AGVruta.setRows(5);
        AGVruta.setBorder(javax.swing.BorderFactory.createTitledBorder("Bluetoothkommunikation"));
        ScrollAGVruta.setViewportView(AGVruta);
        AGVruta.getAccessibleContext().setAccessibleName("Tidsstämpel, Koordinat, Status");

        HTTPruta.setColumns(20);
        HTTPruta.setRows(5);
        HTTPruta.setBorder(javax.swing.BorderFactory.createTitledBorder("HTTP"));
        ScrollHTTPruta.setViewportView(HTTPruta);
        HTTPruta.getAccessibleContext().setAccessibleName("HTTP");

        StoppKnapp.setBackground(new java.awt.Color(255, 0, 0));
        StoppKnapp.setText("STOPP");
        StoppKnapp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                StoppKnappActionPerformed(evt);
            }
        });

        CheckKnapp.setBackground(new java.awt.Color(255, 215, 0));
        CheckKnapp.setLabel("CHECK");
        CheckKnapp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                CheckKnappActionPerformed(evt);
            }
        });

        RuttKnapp.setLabel("Beräkna rutt");
        RuttKnapp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                RuttKnappActionPerformed(evt);
            }
        });

        pos2Knapp.setBackground(new java.awt.Color(153, 255, 204));
        pos2Knapp.setText("Pos. 2");
        pos2Knapp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                pos2KnappActionPerformed(evt);
            }
        });

        pos1Knapp.setBackground(new java.awt.Color(153, 255, 204));
        pos1Knapp.setText("Pos. 1");
        pos1Knapp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                pos1KnappActionPerformed(evt);
            }
        });

        RUTTruta.setColumns(20);
        RUTTruta.setRows(5);
        RUTTruta.setBorder(javax.swing.BorderFactory.createTitledBorder("Ändring av position"));
        RUTTruta.setName(""); // NOI18N
        RUTTruta.setPreferredSize(new java.awt.Dimension(500, 200));
        ScrollRUTTruta.setViewportView(RUTTruta);
        RUTTruta.getAccessibleContext().setAccessibleName("Rutt-koordinater");

        enterKnapp.setText("Enter");
        enterKnapp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                enterKnappActionPerformed(evt);
            }
        });

        claimKnapp.setText("Claim");
        claimKnapp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                claimKnappActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
                layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGroup(layout.createSequentialGroup()
                                .addContainerGap()
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                        .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                        .addGroup(layout.createSequentialGroup()
                                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                                        .addComponent(ScrollRUTTruta)
                                                        .addGroup(layout.createSequentialGroup()
                                                                .addComponent(nyStartRuta, javax.swing.GroupLayout.PREFERRED_SIZE, 270, javax.swing.GroupLayout.PREFERRED_SIZE)
                                                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                                                .addComponent(enterKnapp)
                                                                .addGap(0, 0, Short.MAX_VALUE))
                                                        .addGroup(layout.createSequentialGroup()
                                                                .addComponent(RuttKnapp)
                                                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                                                .addComponent(pos1Knapp)
                                                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                                                .addComponent(pos2Knapp, javax.swing.GroupLayout.PREFERRED_SIZE, 85, javax.swing.GroupLayout.PREFERRED_SIZE)))
                                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                                .addComponent(ScrollAGVruta, javax.swing.GroupLayout.DEFAULT_SIZE, 267, Short.MAX_VALUE)
                                                .addGap(12, 12, 12)
                                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                                        .addComponent(ScrollHTTPruta, javax.swing.GroupLayout.DEFAULT_SIZE, 268, Short.MAX_VALUE)
                                                        .addGroup(layout.createSequentialGroup()
                                                                .addComponent(claimKnapp, javax.swing.GroupLayout.PREFERRED_SIZE, 93, javax.swing.GroupLayout.PREFERRED_SIZE)
                                                                .addGap(0, 0, Short.MAX_VALUE)))
                                                .addContainerGap())
                                        .addGroup(layout.createSequentialGroup()
                                                .addComponent(StartKnapp)
                                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                                .addComponent(StoppKnapp)
                                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                                .addComponent(CheckKnapp)
                                                .addGap(0, 0, Short.MAX_VALUE))))
        );
        layout.setVerticalGroup(
                layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGroup(layout.createSequentialGroup()
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                                                .addComponent(StartKnapp, javax.swing.GroupLayout.PREFERRED_SIZE, 39, javax.swing.GroupLayout.PREFERRED_SIZE)
                                                .addComponent(StoppKnapp, javax.swing.GroupLayout.PREFERRED_SIZE, 41, javax.swing.GroupLayout.PREFERRED_SIZE))
                                        .addComponent(CheckKnapp, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                        .addComponent(ScrollAGVruta)
                                        .addGroup(layout.createSequentialGroup()
                                                .addComponent(ScrollHTTPruta, javax.swing.GroupLayout.PREFERRED_SIZE, 0, Short.MAX_VALUE)
                                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                                .addComponent(claimKnapp, javax.swing.GroupLayout.PREFERRED_SIZE, 33, javax.swing.GroupLayout.PREFERRED_SIZE)
                                                .addContainerGap())
                                        .addGroup(layout.createSequentialGroup()
                                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                                                        .addComponent(nyStartRuta)
                                                        .addComponent(enterKnapp, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE, false)
                                                        .addComponent(RuttKnapp, javax.swing.GroupLayout.DEFAULT_SIZE, 29, Short.MAX_VALUE)
                                                        .addComponent(pos2Knapp, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                                        .addComponent(pos1Knapp, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                                .addComponent(ScrollRUTTruta))))
        );

        // copy paste till hit
        RUTTruta.append(ds.routePlan);
        HTTPruta.append(ds.otherPos);
        // System.out.println(ds.allTasksList);
//        RUTTruta.append(this.ds.infoText + "\n" + ds.nyStart + "\n");
        AGVruta.append(ds.command);
//        AGVruta.append(getTimeStamp());
//        HTTPruta.append(ds.assignURL);

        //  jTextArea2.append(this.ds.routeNodes);
        pack();
    }// </editor-fold>                              
//   //Write in Textarea1

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jPanel1 = new javax.swing.JPanel();
        StartKnapp = new javax.swing.JButton();
        ScrollAGVruta = new javax.swing.JScrollPane();
        AGVruta = new javax.swing.JTextArea();
        ScrollHTTPruta = new javax.swing.JScrollPane();
        HTTPruta = new javax.swing.JTextArea();
        StoppKnapp = new javax.swing.JButton();
        CheckKnapp = new javax.swing.JButton();
        RuttKnapp = new javax.swing.JButton();
        nyStartRuta = new javax.swing.JTextField();
        pos2Knapp = new javax.swing.JButton();
        pos1Knapp = new javax.swing.JButton();
        ScrollRUTTruta = new javax.swing.JScrollPane();
        RUTTruta = new javax.swing.JTextArea();
        enterKnapp = new javax.swing.JButton();
        claimKnapp = new javax.swing.JButton();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        setExtendedState(6);

        jPanel1.setBackground(new java.awt.Color(255, 255, 255));

        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 0, Short.MAX_VALUE)
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 274, Short.MAX_VALUE)
        );

        StartKnapp.setBackground(new java.awt.Color(0, 204, 0));
        StartKnapp.setText("START");
        StartKnapp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                StartKnappActionPerformed(evt);
            }
        });

        AGVruta.setColumns(20);
        AGVruta.setRows(5);
        AGVruta.setBorder(javax.swing.BorderFactory.createTitledBorder("X. Uppdrag: Status"));
        ScrollAGVruta.setViewportView(AGVruta);
        AGVruta.getAccessibleContext().setAccessibleName("Tidsstämpel, Koordinat, Status");

        HTTPruta.setColumns(20);
        HTTPruta.setRows(5);
        HTTPruta.setBorder(javax.swing.BorderFactory.createTitledBorder("Felmeddelanden"));
        ScrollHTTPruta.setViewportView(HTTPruta);
        HTTPruta.getAccessibleContext().setAccessibleName("HTTP");

        StoppKnapp.setBackground(new java.awt.Color(255, 0, 0));
        StoppKnapp.setText("STOPP");
        StoppKnapp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                StoppKnappActionPerformed(evt);
            }
        });

        CheckKnapp.setBackground(new java.awt.Color(255, 215, 0));
        CheckKnapp.setLabel("CHECK");
        CheckKnapp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                CheckKnappActionPerformed(evt);
            }
        });

        RuttKnapp.setLabel("Beräkna rutt");
        RuttKnapp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                RuttKnappActionPerformed(evt);
            }
        });

        pos2Knapp.setBackground(new java.awt.Color(153, 255, 204));
        pos2Knapp.setText("Pos. 2");
        pos2Knapp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                pos2KnappActionPerformed(evt);
            }
        });

        pos1Knapp.setBackground(new java.awt.Color(153, 255, 204));
        pos1Knapp.setText("Pos. 1");
        pos1Knapp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                pos1KnappActionPerformed(evt);
            }
        });

        RUTTruta.setColumns(20);
        RUTTruta.setRows(5);
        RUTTruta.setBorder(javax.swing.BorderFactory.createTitledBorder("Koordinater"));
        RUTTruta.setName(""); // NOI18N
        RUTTruta.setPreferredSize(new java.awt.Dimension(500, 200));
        ScrollRUTTruta.setViewportView(RUTTruta);
        RUTTruta.getAccessibleContext().setAccessibleName("Rutt-koordinater");

        enterKnapp.setText("Enter");
        enterKnapp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                enterKnappActionPerformed(evt);
            }
        });

        claimKnapp.setText("Claim");
        claimKnapp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                claimKnappActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(ScrollRUTTruta)
                            .addGroup(layout.createSequentialGroup()
                                .addComponent(nyStartRuta, javax.swing.GroupLayout.PREFERRED_SIZE, 270, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(enterKnapp)
                                .addGap(0, 0, Short.MAX_VALUE))
                            .addGroup(layout.createSequentialGroup()
                                .addComponent(RuttKnapp)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                .addComponent(pos1Knapp)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(pos2Knapp, javax.swing.GroupLayout.PREFERRED_SIZE, 85, javax.swing.GroupLayout.PREFERRED_SIZE)))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(ScrollAGVruta, javax.swing.GroupLayout.DEFAULT_SIZE, 267, Short.MAX_VALUE)
                        .addGap(12, 12, 12)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(ScrollHTTPruta, javax.swing.GroupLayout.DEFAULT_SIZE, 268, Short.MAX_VALUE)
                            .addGroup(layout.createSequentialGroup()
                                .addComponent(claimKnapp, javax.swing.GroupLayout.PREFERRED_SIZE, 93, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addGap(0, 0, Short.MAX_VALUE)))
                        .addContainerGap())
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(StartKnapp)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(StoppKnapp)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(CheckKnapp)
                        .addGap(0, 0, Short.MAX_VALUE))))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                    .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                        .addComponent(StartKnapp, javax.swing.GroupLayout.PREFERRED_SIZE, 39, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(StoppKnapp, javax.swing.GroupLayout.PREFERRED_SIZE, 41, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addComponent(CheckKnapp, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(ScrollAGVruta)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(ScrollHTTPruta, javax.swing.GroupLayout.PREFERRED_SIZE, 0, Short.MAX_VALUE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(claimKnapp, javax.swing.GroupLayout.PREFERRED_SIZE, 33, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addContainerGap())
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                            .addComponent(nyStartRuta)
                            .addComponent(enterKnapp, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE, false)
                            .addComponent(RuttKnapp, javax.swing.GroupLayout.DEFAULT_SIZE, 29, Short.MAX_VALUE)
                            .addComponent(pos2Knapp, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                            .addComponent(pos1Knapp, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(ScrollRUTTruta))))
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void StartKnappActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_StartKnappActionPerformed
        // Skicka "Begin"
        ds.command = getTimeStamp() + "_B";
        AGVruta.append("SKICKAR: " + getTimeStamp() + "_B\n");
        ds.beginPos = true;
    }//GEN-LAST:event_StartKnappActionPerformed

    private void StoppKnappActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_StoppKnappActionPerformed
        // Skicka "Stop"
        ds.command = getTimeStamp() + "_S";
        AGVruta.append("SKICKAR: " + getTimeStamp() + "_S\n");
    }//GEN-LAST:event_StoppKnappActionPerformed

    private void CheckKnappActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_CheckKnappActionPerformed
        // Skicka "Confirm"
        ds.command = getTimeStamp() + "_C";
        AGVruta.append("SKICKAR: " + getTimeStamp() + "_C\n");
    }//GEN-LAST:event_CheckKnappActionPerformed

    private void RuttKnappActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_RuttKnappActionPerformed
        // Beräkna rutt knapp
        System.out.println("Skriv det ut?");
        OptPlan op = new OptPlan(ds);
        op.createPlan();
        ds.routeProtocol = getTimeStamp() + "_" + ds.newStartCo + "_" + ds.routeCom + ds.endKo + "_D_F\n";
        ds.command = ds.routeProtocol;
        AGVruta.append("\nSKICKAR: " + ds.routeProtocol + "\n");

    }//GEN-LAST:event_RuttKnappActionPerformed

    private void pos2KnappActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_pos2KnappActionPerformed
        RUTTruta.append("\n Du tryckte på Pos.2 (Du är dominant) \n");
        ds.routeCom = "";
        ds.newStart = 44;
        ds.newStartCo = "000060";
        ds.xAGV = "000";
        ds.yAGV = "060";
        ds.id = 2;
        ds.wishList = ds.wishListPos2;
    }//GEN-LAST:event_pos2KnappActionPerformed

    private void pos1KnappActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_pos1KnappActionPerformed
        RUTTruta.append("\n Du tryckte på Pos.1 (Du är passiv) \n");
        ds.newStart = 132;
        ds.routeCom = "";
        ds.newStartCo = "000180";
        ds.xAGV = "000";
        ds.yAGV = "180";
        ds.id = 1;
        ds.wishList = ds.wishListPos1;
    }//GEN-LAST:event_pos1KnappActionPerformed

    private void enterKnappActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_enterKnappActionPerformed
        // enter-knappen
        newInfo();
        pos1Knapp.setEnabled(false);
        pos2Knapp.setEnabled(false);

    }//GEN-LAST:event_enterKnappActionPerformed

    private void claimKnappActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_claimKnappActionPerformed
        // TODO add your handling code here:
        ds.httpStart = true;
    }//GEN-LAST:event_claimKnappActionPerformed

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(ControlUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(ControlUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(ControlUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(ControlUI.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new ControlUI().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JTextArea AGVruta;
    private javax.swing.JButton CheckKnapp;
    private javax.swing.JTextArea HTTPruta;
    private javax.swing.JTextArea RUTTruta;
    private javax.swing.JButton RuttKnapp;
    private javax.swing.JScrollPane ScrollAGVruta;
    private javax.swing.JScrollPane ScrollHTTPruta;
    private javax.swing.JScrollPane ScrollRUTTruta;
    private javax.swing.JButton StartKnapp;
    private javax.swing.JButton StoppKnapp;
    private javax.swing.JButton claimKnapp;
    private javax.swing.JButton enterKnapp;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JTextField nyStartRuta;
    private javax.swing.JButton pos1Knapp;
    private javax.swing.JButton pos2Knapp;
    // End of variables declaration//GEN-END:variables
}
