package com.example.team3_project;


import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;

public class User_Login extends AppCompatActivity {

    Button btn_uSignup, btn_uLogin, btn_aLogin;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.user_login);
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO); //다크모드 해제

        btn_uSignup = findViewById(R.id.btnUser_signup);
        btn_uLogin = findViewById(R.id.btnUser_Login);
        btn_aLogin = findViewById(R.id.btnAdmin_login);

        //사용자 회원가입 버튼 클릭
        btn_uSignup.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(User_Login.this, User_SignUp.class); //화면 전환
                startActivity(intent);
            }
        });

        //사용자 계정 로그인 버튼 클릭
        btn_uLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(User_Login.this, MainActivity.class); //화면 전환
                startActivity(intent);
            }
        });

        //관리자 계정 로그인 버튼 클릭
        btn_aLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(User_Login.this, Admin_Login.class); //화면 전환
                startActivity(intent);
            }
        });

    }

}