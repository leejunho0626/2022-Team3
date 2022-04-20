package com.example.team3_project;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;
import androidx.core.app.ActivityCompat;

//앱 실행 시작화면
public class Login_Choice extends AppCompatActivity {

    Button btnUser, btnAdmin;
    private long backPressedTime = 0;
    private final long FINISH_INTERVAL_TIME = 2000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login_choice);
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO); //다크모드 해제

        btnUser = findViewById(R.id.btnUser);
        btnAdmin = findViewById(R.id.btnAdmin);

        //검사원 버튼 클릭
        btnUser.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(Login_Choice.this, User_Login.class); //화면 전환
                startActivity(intent); //사용자 회원가입 화면으로 이동
            }
        });
        //총괄자 버튼 클릭
        btnAdmin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(Login_Choice.this, Admin_Login.class); //화면 전환
                startActivity(intent); //사용자 회원가입 화면으로 이동
            }
        });


    }

    //뒤로가기 버튼(종료)
    public void onBackPressed() {
        long tempTime = System.currentTimeMillis();
        long intervalTime = tempTime - backPressedTime;
        if (0 <= intervalTime && FINISH_INTERVAL_TIME >= intervalTime) {
            super.onBackPressed();
            ActivityCompat.finishAffinity(this);
            System.exit(0);
        }
        else {
            backPressedTime = tempTime;
            Toast.makeText(this, "뒤로 버튼을 한번 더 누르시면 종료됩니다.", Toast.LENGTH_SHORT).show();
        }
    }
}
