package com.example.team3_project;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;


import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.HashMap;
import java.util.Map;

public class Admin_SignUp extends AppCompatActivity {

    TextView txtErr;
    Button btn_aFinish;
    EditText edt_aID;
    private FirebaseDatabase database = FirebaseDatabase.getInstance();
    private DatabaseReference databaseReference = database.getReference();

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.admin_signup);
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO); //다크모드 해제

        txtErr = findViewById(R.id.txtErr);
        btn_aFinish = findViewById(R.id.btn_aFinish);
        edt_aID = findViewById(R.id.edt_aID);

        //버튼 활성/비활성화
        edt_aID.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void afterTextChanged(Editable editable) {
                if(editable.length()>0){
                    btn_aFinish.setBackgroundColor(getResources().getColor(R.color.orange));
                    btn_aFinish.setClickable(true);
                }
                else{
                    btn_aFinish.setBackgroundColor(Color.GRAY);
                    btn_aFinish.setClickable(false);
                }

            }
        });

        //관리자 등록 완료 버튼 클릭
        btn_aFinish.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                saveAdmin(edt_aID.getText().toString());
            }
        });

    }
    
    //관리자 등록(중복검사)
    public void saveAdmin(String aID){
        Map<String, Object> info = new HashMap<>();
        info.put("id", aID);
            databaseReference.child(aID).addValueEventListener(new ValueEventListener() {
                @Override
                //데이터 존재 유무 검사
                public void onDataChange(@NonNull DataSnapshot snapshot) {
                    //예외처리 
                    //이미 등록된 번호일 때
                    try{
                        String data = snapshot.getValue().toString();
                        if(data != null){
                            txtErr.setVisibility(View.VISIBLE);
                        }

                    }
                    //신규 등록일 때
                    catch (NullPointerException e){
                        databaseReference.child(aID).setValue(info);
                        Toast.makeText(getApplicationContext(), "등록되었습니다.", Toast.LENGTH_SHORT).show();
                        Intent intent = new Intent(Admin_SignUp.this, Admin_Login.class); //화면 전환
                        intent.addFlags(intent.FLAG_ACTIVITY_CLEAR_TOP);
                        startActivity(intent);
                    }

                }
                @Override
                public void onCancelled(@NonNull DatabaseError error) {

                }
            });

    }

}