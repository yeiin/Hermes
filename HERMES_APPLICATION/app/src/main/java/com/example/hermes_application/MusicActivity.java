package com.example.hermes_application;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Message;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class MusicActivity extends AppCompatActivity {
    private final String Action = "MainActivity_Action";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_music);

        Button button_previous = (Button) findViewById(R.id.button_third);
        Button btn_music_one = (Button) findViewById(R.id.music_a);
        Button btn_music_two = (Button) findViewById(R.id.music_b);

        button_previous.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });
        btn_music_one.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View view) {
                //socket 통신으로 55 전송
                String msg = "55";
                Intent intent = new Intent(Action);
                intent.putExtra("music", msg);
                sendBroadcast(intent);
                Toast.makeText(getApplicationContext(), "Music 1 is selected", Toast.LENGTH_SHORT).show();
                return true;

            }
        });
        btn_music_two.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View view) {
                //socket 통신으로 555 전송
                String msg = "555";
                Intent intent = new Intent(Action);
                intent.putExtra("music", msg);
                sendBroadcast(intent);
                Toast.makeText(getApplicationContext(), "Music 2 is selected", Toast.LENGTH_SHORT).show();
                return true;
            }
        });
    }
}