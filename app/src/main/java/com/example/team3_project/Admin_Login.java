package com.example.team3_project;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;

public class Admin_Login extends AppCompatActivity {

    Button btn_aLogin, btn_aRegister;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.admin_login);
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO); //다크모드 해제

        btn_aLogin = findViewById(R.id.btn_aLogin);
        btn_aRegister = findViewById(R.id.btn_aRegister);

        //관리자 로그인 버튼 클릭
        btn_aLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(Admin_Login.this, All_DataList.class); //화면 전환
                startActivity(intent);
            }
        });
        //관리자 등록 버튼 클릭
        btn_aRegister.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(Admin_Login.this, Admin_SignUp.class); //화면 전환
                startActivity(intent);
            }
        });


    }

}