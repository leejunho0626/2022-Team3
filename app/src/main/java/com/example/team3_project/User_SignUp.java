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

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class User_SignUp extends AppCompatActivity {

    Button btn_uConfirm;
    EditText edt_uID, edt_uPW, edt_uPW2;
    private FirebaseAuth firebaseAuth; //FirebaseAuth 선언
    private FirebaseDatabase database = FirebaseDatabase.getInstance();
    private DatabaseReference databaseReference = database.getReference();


    @Override
    protected void onCreate(Bundle savedInstanceState) {



        super.onCreate(savedInstanceState);
        setContentView(R.layout.user_signup);
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO); //다크모드 해제

        btn_uConfirm = findViewById(R.id.btn_uConfirm);
        edt_uID = findViewById(R.id.edt_uID);
        edt_uPW = findViewById(R.id.edt_uPW);
        edt_uPW2 = findViewById(R.id.edt_uPW2);

        firebaseAuth = FirebaseAuth.getInstance();

        //사용자 회원가입 완료 버튼 클릭
        btn_uConfirm.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                final String id = edt_uID.getText().toString().trim();
                final String pw = edt_uPW2.getText().toString().trim();
                //입력한 아이디와 비밀번호가 있을 경우
                if(id.length()>0&&pw.length()>0){
                    firebaseAuth.createUserWithEmailAndPassword(id, pw).addOnCompleteListener(User_SignUp.this, new OnCompleteListener<AuthResult>() {
                        @Override
                        public void onComplete(@NonNull Task<AuthResult> task) {
                            //계정 생성 성공
                            if (task.isSuccessful()) {
                                Toast.makeText(getApplicationContext(), "회원가입을 축하합니다.", Toast.LENGTH_SHORT).show();
                                Intent intent = new Intent(User_SignUp.this, User_Login.class); //화면 전환
                                startActivity(intent);
                                finish();
                            }
                            else{
                                Toast.makeText(getApplicationContext(), "회원가입 실패.", Toast.LENGTH_SHORT).show();
                            }
                        }
                    });
                }
                else{
                    Toast.makeText(getApplicationContext(),"아이디 또는 비밀번호를 입력하세요.",Toast.LENGTH_SHORT).show();
                }

            }
        });

    }
}