package com.example.team3_project;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class Admin_Login extends AppCompatActivity {

    Button btn_aLogin, btn_aRegister;
    EditText login_AdminID;
    private FirebaseDatabase database = FirebaseDatabase.getInstance();
    private DatabaseReference databaseReference = database.getReference();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.admin_login);
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO); //다크모드 해제

        btn_aLogin = findViewById(R.id.btn_aLogin);
        btn_aRegister = findViewById(R.id.btn_aRegister);
        login_AdminID = findViewById(R.id.login_AdminID);

        //관리자 로그인 버튼 클릭
        btn_aLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                aLogin(login_AdminID.getText().toString());

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

    //관리자 로그인
    public void aLogin(String aID){
        databaseReference.child(aID).addValueEventListener(new ValueEventListener() {
            @Override
            //데이터 존재 유무 검사
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                //예외처리
                //등록된 관리자 번호 일치 -> 로그인성공
                try{
                    String data = snapshot.getValue().toString();
                    Intent intent = new Intent(Admin_Login.this, All_DataList.class); //화면 전환
                    intent.addFlags(intent.FLAG_ACTIVITY_CLEAR_TOP);
                    startActivity(intent);
                }
                //로그인 실패
                catch (NullPointerException e){
                    Toast.makeText(getApplicationContext(), "등록되지않거나 잘못된 번호입니다.", Toast.LENGTH_SHORT).show();
                }

            }
            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });
    }


}