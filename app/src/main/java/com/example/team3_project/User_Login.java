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
import androidx.core.app.ActivityCompat;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;

public class User_Login extends AppCompatActivity {

    Button btn_uSignup, btn_uLogin; //버튼 변수 생성
    EditText edt_ID, edt_PW;
    FirebaseAuth firebaseAuth;
    private long backPressedTime = 0;
    private final long FINISH_INTERVAL_TIME = 2000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.user_login);
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO); //다크모드 해제

        //버튼 객체 접근
        btn_uSignup = findViewById(R.id.btnUser_Signup);
        btn_uLogin = findViewById(R.id.btnUser_Login);

        edt_ID = findViewById(R.id.edt_loginID);
        edt_PW = findViewById(R.id.edt_loginPW);

        firebaseAuth = FirebaseAuth.getInstance();

        //자동로그인(로그아웃을 하지 않고 종료한 경우)
        if(firebaseAuth.getCurrentUser() != null){
            Intent intent = new Intent(this, MainActivity.class); //메인화면으로 이동
            startActivity(intent);
            finish();
        }

        //사용자 회원가입 버튼 클릭
        btn_uSignup.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(User_Login.this, User_SignUp.class); //화면 전환
                startActivity(intent); //사용자 회원가입 화면으로 이동
            }
        });

        //사용자 계정 로그인 버튼 클릭
        btn_uLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                uLogin(edt_ID.getText().toString(), edt_PW.getText().toString());
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
    //일반 로그인(파이어베이스)
    public void uLogin(String id, String pw){
        id = edt_ID.getText().toString().trim(); //아이디
        pw = edt_PW.getText().toString().trim(); //비밀번호
        //입력한 아이디, 비밀번호가 있는 경우
        if(id.length()>0 && pw.length()>0){
            firebaseAuth.signInWithEmailAndPassword(id, pw)
                    .addOnCompleteListener(this, new OnCompleteListener<AuthResult>() {
                        @Override
                        public void onComplete(@NonNull Task<AuthResult> task) {
                            if(task.isSuccessful()){
                                Intent intent = new Intent(User_Login.this, MainActivity.class); //메인화면으로 이동
                                intent.addFlags(intent.FLAG_ACTIVITY_CLEAR_TOP);
                                startActivity(intent);
                            }
                            else {
                                Toast.makeText(getApplicationContext(),"아이디 또는 비밀번호가 틀렸습니다.",Toast.LENGTH_SHORT).show();
                            }
                        }
                    });
        }
        else{
            Toast.makeText(getApplicationContext(),"아이디 또는 비밀번호를 입력하세요.",Toast.LENGTH_SHORT).show();
        }
    }

}