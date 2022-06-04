package com.example.team3_project;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.firestore.FirebaseFirestore;

import java.util.HashMap;
import java.util.Map;

import static android.content.ContentValues.TAG;

public class User_SignUp extends AppCompatActivity {

    Button btn_uConfirm;
    EditText edt_uID, edt_uPW;
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


        firebaseAuth = FirebaseAuth.getInstance();

        //사용자 회원가입 완료 버튼 클릭
        btn_uConfirm.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                final String id = edt_uID.getText().toString().trim();
                final String pw = edt_uPW.getText().toString().trim();
                //입력한 아이디와 비밀번호가 있을 경우
                if(id.length()>0&&pw.length()>0){
                    firebaseAuth.createUserWithEmailAndPassword(id, pw).addOnCompleteListener(User_SignUp.this, new OnCompleteListener<AuthResult>() {
                        @Override
                        public void onComplete(@NonNull Task<AuthResult> task) {
                            //계정 생성 성공
                            if (task.isSuccessful()) {
                                Map<String, Object> info = new HashMap<>();
                                FirebaseUser user = FirebaseAuth.getInstance().getCurrentUser();
                                info.put("id", user.getEmail());
                                info.put("pw", pw);
                                saveID();
                                databaseReference.child(user.getUid()).setValue(info);
                                Toast.makeText(getApplicationContext(), "회원가입을 축하합니다.", Toast.LENGTH_SHORT).show();
                                Intent intent = new Intent(User_SignUp.this, User_Login.class); //화면 전환
                                startActivity(intent);
                                finish();
                            }
                            else{
                                Toast.makeText(getApplicationContext(), "회원가입 진행을 다시 해주세요.", Toast.LENGTH_SHORT).show();
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
    //파이어스토어에 ID 저장
    public void saveID(){
        Map<String, Object> id = new HashMap<>();
        FirebaseUser user = FirebaseAuth.getInstance().getCurrentUser();
        FirebaseFirestore db = FirebaseFirestore.getInstance();
        id.put("id", user.getEmail());
        db.collection("User").document(user.getEmail()).set(id) //경로
                .addOnSuccessListener(new OnSuccessListener<Void>() {
                    @Override
                    public void onSuccess(Void avoid) {
                        Log.i(TAG, "success");
                    }
                })
                .addOnFailureListener(new OnFailureListener() {
                    @Override
                    public void onFailure(@NonNull Exception e) {
                        Log.i(TAG, "fail");
                    }
                });
    }
}