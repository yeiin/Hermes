package com.example.hermes_application;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.DataOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;

public class MainActivity extends AppCompatActivity {

    public static Context mContext;
    private final String Action = "MainActivity_Action";
    private Handler mHandler;
    private Socket socket;
    private String ip = "192.168.0.17"; //server's IP
    private int port = 12345; //port number
    private BroadcastReceiver mReceiver = null;
    TextView text_connection;
    public Handler SendHandler;

    public static final String TAG = "MainActivity";

    private void registerReceiver() {
        int mess = 1010;
        if(mReceiver != null) return;
        final IntentFilter intentFilter = new IntentFilter();
        intentFilter.addAction(Action);
        this.mReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
//                Log.d(TAG, "This is onReceive()");
                String receivedData = intent.getStringExtra("music");
                Log.d(TAG, "@@@@@@@@@@@@@@@@ : "+receivedData);
                if(intent.getAction().equals(Action))
                {
                    Message message = Message.obtain();
                    message.obj = ""+receivedData;
                    SendHandler.sendMessage(message);
                }
            }
        };
        this.registerReceiver(this.mReceiver, intentFilter);
    }

    @RequiresApi(api = Build.VERSION_CODES.M)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        registerReceiver();
        String[] Permissions = new String[]{Manifest.permission.RECORD_AUDIO, Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.READ_EXTERNAL_STORAGE};
        requestPermissions(Permissions,0x00000001);

        mContext = this;

        mHandler = new Handler();

        text_connection = (TextView) findViewById(R.id.textView_connection);
        TextView text_mobile = (TextView) findViewById(R.id.textView_mobile);
        TextView text_led = (TextView) findViewById(R.id.textView_LED);
        TextView text_illuminance = (TextView) findViewById(R.id.textView_illuminance);
        TextView text_music = (TextView) findViewById(R.id.textView_music);
        TextView text_mode = (TextView) findViewById(R.id.textView_mode);

        Button btn_state = (Button) findViewById(R.id.button_first);
        Button btn_connection = (Button) findViewById(R.id.button_connection);
        Button btn_mobile = (Button) findViewById(R.id.button_mobile);
        Button btn_led = (Button) findViewById(R.id.button_led);
        Button btn_illuminance = (Button) findViewById(R.id.button_illuminance);
        Button btn_music = (Button) findViewById(R.id.button_music);
        Button btn_mode = (Button) findViewById(R.id.button_mode);

        Context context = this;

        //Click connect button
        btn_connection.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                //text_connection의 text가 OFF일 때, socket connect 요청
                if (text_connection.getText().toString().equals("OFF")) {
                    ReceiveThread receivethread = null;
                    try {
                        receivethread = new ReceiveThread();
//                        Log.d("Finish Connection!","success receive_thread");
                    } catch (IOException e) {
                        e.printStackTrace();
//                        Log.d("Failed Connection!","fail receive_thread");
                    }
                    receivethread.start();
                    SendThread sendThread = null;
                    try {
                        sendThread = new SendThread();
//                        Log.d("Finish Connection!", "success send_thread");
                    } catch (IOException e) {
                        e.printStackTrace();
//                        Log.d("Failed Connection!","fail send_thread");
                    }
                    sendThread.start();
                    text_connection.setText("ON");
                }
                else if (text_connection.getText().toString().equals("ON")) {
                    //disconnect socket
                    try {
                        socket.close();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    text_connection.setText("OFF");
                    Toast.makeText(getApplicationContext(), "Stop Connecting", Toast.LENGTH_SHORT).show();
                }
            }
        });


        //long click
        btn_state.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View view) {
                Intent intent = new Intent(context, BabyVideoActivity.class);
                startActivity(intent);
                Toast.makeText(getApplicationContext(), "This is Video", Toast.LENGTH_SHORT).show();
                return true;
            }
        });
        btn_music.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View view) {
                Intent intent = new Intent(context, MusicActivity.class);
                startActivity(intent);
                Toast.makeText(getApplicationContext(), "Select Music", Toast.LENGTH_SHORT).show();
                return true;
            }
        });


        //basic click
        btn_mobile.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(text_mobile.getText().toString().equals("OFF")) {
                    //socket 통신으로 2 전송
                    String msg = "2";
                    Message message = Message.obtain();
                    message.obj = msg;
                    SendHandler.sendMessage(message);
                    text_mobile.setText("ON");
                }
                else if(text_mobile.getText().toString().equals("ON")) {
                    //socket 통신으로 22 전송
                    String msg = "22";
                    Message message = Message.obtain();
                    message.obj = msg;
                    SendHandler.sendMessage(message);
                    text_mobile.setText("OFF");
                }
            }
        });
        btn_led.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(text_led.getText().toString().equals("OFF")) {
                    //socket 통신으로 3 전송
                    String msg = "3";
                    Message message = Message.obtain();
                    message.obj = msg;
                    SendHandler.sendMessage(message);
                    text_led.setText("ON");
                }
                else if(text_led.getText().toString().equals("ON")) {
                    //socket 통신으로 33 전송
                    String msg = "33";
                    Message message = Message.obtain();
                    message.obj = msg;
                    SendHandler.sendMessage(message);
                    text_led.setText("OFF");
                }
            }
        });
        btn_music.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(text_music.getText().toString().equals("PLAY")) {
                    //socket 통신으로 5 전송
                    String msg = "5";
                    Message message = Message.obtain();
                    message.obj = msg;
                    SendHandler.sendMessage(message);
                    text_music.setText("STOP");
                }
                else if(text_music.getText().toString().equals("STOP")) {
                    //화면 전환
                    Intent intent = new Intent(context, MusicActivity.class);
                    startActivity(intent);
                    Toast.makeText(getApplicationContext(), "Select Music", Toast.LENGTH_SHORT).show();
                }
            }
        });

//        btn_illuminance.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View view) {
//                if(text_illuminance.getText().toString().equals("OFF")) {
//                    //socket 통신으로 4 전송
//                    String msg = "4";
//                    Message message = Message.obtain();
//                    message.obj = msg;
//                    SendHandler.sendMessage(message);
//                    text_illuminance.setText("ON");
//                }
//                else if(text_illuminance.getText().toString().equals("ON")) {
//                    //socket 통신으로 44 전송
//                    String msg = "44";
//                    Message message = Message.obtain();
//                    message.obj = msg;
//                    SendHandler.sendMessage(message);
//                    text_illuminance.setText("OFF");
//                }
//            }
//        });
        btn_mode.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(text_mode.getText().toString().equals("USER")) {
                    //socket 통신으로 6 전송
                    String msg = "6";
                    Message message = Message.obtain();
                    message.obj = msg;
                    SendHandler.sendMessage(message);
                    text_mode.setText("AUTO");
                }
                else if(text_mode.getText().toString().equals("AUTO")) {
                    //socket 통신으로 66 전송
                    String msg = "66";
                    Message message = Message.obtain();
                    message.obj = msg;
                    SendHandler.sendMessage(message);
                    text_mode.setText("USER");
                }
            }
        });
    }

    class ReceiveThread extends Thread {
        private final String Action2 = "VoiceActivity_Action";

        public ReceiveThread() throws IOException {
//            Log.d("In Receive Thread","Receive Thread 1");
        }
        @Override
        public void run() {
            try {
                //create socket
                socket = new Socket(ip, port);
                if (socket != null) {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(getApplicationContext(), "Success Connecting", Toast.LENGTH_SHORT).show();
                        }
                    });
                }
                else {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(getApplicationContext(), "Failed Connecting", Toast.LENGTH_SHORT).show();
                        }
                    });
                }
//                Log.d("In Receive Thread","Receive Thread 2 : " + socket);

                //receive data
                while(true)
                {
//                    Log.d("In Receive Thread","Receive Thread 3");
                    while(socket.getInputStream().available()< 0);
                    byte[] buffer = new byte[100];
                    socket.getInputStream().read(buffer);
//                    Log.d("In Receive Thread","Receive Thread 4");
                    for(int i = 0; i<buffer.length; i++)
                    {
//                        Log.d(TAG, "///////////////////////// run: buffer " + buffer[i]);
                    }
//                    ByteArrayInputStream byteArrayInputStream = new ByteArrayInputStream(buffer);
//                    Log.d(TAG, "------------------- byteArrayInputStream : " + byteArrayInputStream);
//                    DataInputStream dataInputStream = new DataInputStream(byteArrayInputStream);
//                    Log.d(TAG, "------------------- dataInputStream : " + dataInputStream);
//                    String read = dataInputStream.readUTF();
//                    Log.d(TAG,"////////////////////////////////// read : " + read);
//                    char[] charArray = read.toCharArray();
//                    Log.d(TAG, "!!!!!!!!!!!!!!! charArray : " + charArray);

                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            //state of baby
                            if(buffer[0] == 48) //0
                            {
                                TextView text = findViewById(R.id.textView_babystate);
                                text.setText("Asleep");
                            }
                            else if(buffer[0] == 49) //1
                            {
                                TextView text = findViewById(R.id.textView_babystate);
                                text.setText("Awake");
                            }
                            else if(buffer[0] == 50) //2
                            {
                                TextView text = findViewById(R.id.textView_babystate);
                                text.setText("Sleep");
                            }
                            else if(buffer[0] == 51) //3
                            {
                                TextView text = findViewById(R.id.textView_babystate);
                                text.setText("Wake");
                            }
                            else //4
                            {
                                TextView text = findViewById(R.id.textView_babystate);
                                text.setText("Detect X");
                            }

                            //mobile
                            if(buffer[1] == 48)
                            {
                                TextView text = findViewById(R.id.textView_mobile);
                                text.setText("OFF");
                            }
                            else
                            {
                                TextView text = findViewById(R.id.textView_mobile);
                                text.setText("ON");
                            }

                            //led
                            if(buffer[2] == 48)
                            {
                                TextView text = findViewById(R.id.textView_LED);
                                text.setText("OFF");
                            }
                            else {
                                TextView text = findViewById(R.id.textView_LED);
                                text.setText("ON");

                            }

                            //music
                            if(buffer[3] == 48) //0
                            {
                                TextView text = findViewById(R.id.textView_music);
                                text.setText("STOP");
                            }
                            else //1
                            {
                                TextView text = findViewById(R.id.textView_music);
                                text.setText("PLAY");
                            }

                            //illuminance
                            if(buffer[4] == 48) //0
                            {
                                TextView text = findViewById(R.id.textView_illuminance);
                                text.setText("LEVEL 0");
//                                Intent intent = new Intent(Action2);
//                                intent.putExtra("Illum", 0);
//                                sendBroadcast(intent);
                            }
                            else if(buffer[4] == 49) //1
                            {
                                TextView text = findViewById(R.id.textView_illuminance);
                                text.setText("LEVEL 1");
//                                Intent intent = new Intent(Action2);
//                                intent.putExtra("Illum", 1);
//                                sendBroadcast(intent);
                            }
                            else if(buffer[4] == 50) //2
                            {
                                TextView text = findViewById(R.id.textView_illuminance);
                                text.setText("LEVEL 2");
//                                Intent intent = new Intent(Action2);
//                                intent.putExtra("Illum", 2);
//                                sendBroadcast(intent);
                            }
                            else if(buffer[4] == 51)
                            {
                                TextView text = findViewById(R.id.textView_illuminance);
                                text.setText("LEVEL 3");
//                                Intent intent = new Intent(Action2);
//                                intent.putExtra("Illum", 3);
//                                sendBroadcast(intent);
                            }
                            else if(buffer[4] == 52)
                            {
                                TextView text = findViewById(R.id.textView_illuminance);
                                text.setText("LEVEL 4");
//                                Intent intent = new Intent(Action2);
//                                intent.putExtra("Illum", 4);
//                                sendBroadcast(intent);
                            }
                            else if(buffer[4] == 53)
                            {
                                TextView text = findViewById(R.id.textView_illuminance);
                                text.setText("LEVEL 5");
//                                Intent intent = new Intent(Action2);
//                                intent.putExtra("Illum", 5);
//                                sendBroadcast(intent);
                            }
                            else if(buffer[4] == 54)
                            {
                                TextView text = findViewById(R.id.textView_illuminance);
                                text.setText("LEVEL 6");
//                                Intent intent = new Intent(Action2);
//                                intent.putExtra("Illum", 6);
//                                sendBroadcast(intent);
                            }
                            else if(buffer[4] == 55)
                            {
                                TextView text = findViewById(R.id.textView_illuminance);
                                text.setText("LEVEL 7");
//                                Intent intent = new Intent(Action2);
//                                intent.putExtra("Illum", 7);
//                                sendBroadcast(intent);
                            }
                            else if(buffer[4] == 56)
                            {
                                TextView text = findViewById(R.id.textView_illuminance);
                                text.setText("LEVEL 8");
//                                Intent intent = new Intent(Action2);
//                                intent.putExtra("Illum", 8);
//                                sendBroadcast(intent);
                            }
                            else if(buffer[4] == 57)
                            {
                                TextView text = findViewById(R.id.textView_illuminance);
                                text.setText("LEVEL 9");
//                                Intent intent = new Intent(Action2);
//                                intent.putExtra("Illum", 9);
//                                sendBroadcast(intent);
                            }
                            else
                            {
                                TextView text = findViewById(R.id.textView_illuminance);
                                text.setText("LEVEL 10");
//                                Intent intent = new Intent(Action2);
//                                intent.putExtra("Illum", 10);
//                                sendBroadcast(intent);
                            }

                            //mode
                            if(buffer[5] == 48)
                            {
                                TextView text = findViewById(R.id.textView_mode);
                                text.setText("AUTO");
                            }
                            else
                            {
                                TextView text = findViewById(R.id.textView_mode);
                                text.setText("USER");
                            }
                        }
                    });
                }

            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    class SendThread extends Thread {
        DataOutputStream dataOutputStream;
        OutputStream outputStream;

        public SendThread() throws IOException {
            Log.d("@@@@/ In Send Thread","Send Thread 1");
        }
        public void run() {
            Log.d("@@@@/ In Send Thread","Send Thread 2");
            while(socket== null);
            Log.d("@@@@/ In Send Thread","Send Thread 3");
            try {
                outputStream = socket.getOutputStream();
                dataOutputStream = new DataOutputStream(outputStream);
                Log.d("@@@@/ In Send Thread","Send Thread 4");
                Log.d("@@@@/ In Send Thread","outputStream : "+outputStream);
                Log.d("@@@@/ In Send Thread","dataOutputStream : "+dataOutputStream);
            } catch (IOException e) {
                e.printStackTrace();
                Log.d("@@@@/ In Send Thread","Send Thread 5");
            }
            Looper.prepare();
            SendHandler = new Handler(Looper.myLooper()) {
                @Override
                public void handleMessage(@NonNull Message msg) {
                    String string = (String)msg.obj;
                    Log.d("@@@@/ In Send Thread","Send Thread 6");
                    Log.d("@@@@/ In Send Thread","String : "+string);
                    try {
//                        string = string + "\n";
                        dataOutputStream.writeUTF(string);
                        dataOutputStream.flush();
//                        dataOutputStream.writeUTF("empty");
//                        dataOutputStream.flush();
                        Log.d("@@@@/ In Send Thread","Send Thread 7");
                        Log.d("@@@@/ In Send Thread","flush dataOutputStream : "+dataOutputStream);
                    } catch (IOException ex) {
                        ex.printStackTrace();
                        Log.d("@@@@/ In Send Thread","Send Thread 8");
                    }
                }
            };
            Looper.loop();
            Log.d("@@@@/ In Send Thread","Send Thread 9");
        }
    }
}
