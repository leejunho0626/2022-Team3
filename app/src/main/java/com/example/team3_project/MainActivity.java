package com.example.team3_project;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;
import androidx.core.app.ActivityCompat;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.QueryDocumentSnapshot;
import com.google.firebase.firestore.QuerySnapshot;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private static Animation fab_open, fab_close;
    private static Boolean isFabOpen = false;
    private static FloatingActionButton fab, fab1;
    FirebaseAuth firebaseAuth;
    FirebaseUser user = FirebaseAuth.getInstance().getCurrentUser();
    private long backPressedTime = 0;
    private final long FINISH_INTERVAL_TIME = 2000;
    TextView txt_uID;
    ArrayList<String> list = new ArrayList<>();
    RecyclerView recyclerView;
    Main_Adapter main_adapter;
    
    //1. Firebase 실시간DB 객체 얻어오기
    FirebaseDatabase firebaseDatabase = FirebaseDatabase.getInstance();
    //2. 저장시킬 노드 참조객체 가져오기
    DatabaseReference ref = firebaseDatabase.getReference(); //()안에 내용이 없으면 최상위 노드

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO); //다크모드 해제

        //플로팅 메뉴 설정
        fab_open = AnimationUtils.loadAnimation(MainActivity.this.getApplicationContext(), R.anim.fab_open);
        fab_close = AnimationUtils.loadAnimation(MainActivity.this.getApplicationContext(), R.anim.fab_close);
        fab = (FloatingActionButton) findViewById(R.id.fab);
        fab1 = (FloatingActionButton) findViewById(R.id.fab1);
        txt_uID = findViewById(R.id.txt_uID);
        firebaseAuth = FirebaseAuth.getInstance();
        main_adapter = new Main_Adapter();
        recyclerView = findViewById(R.id.recyceler_result);
        recyclerView.setLayoutManager(new LinearLayoutManager(MainActivity.this, RecyclerView.VERTICAL, false));

        txt_uID.setText(user.getEmail());
        //show_Result();
        result_check();



        //플로팅메뉴
        fab.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                //
                anim();
            }
        });
        //로그아웃
        fab1.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                //
                anim();
                FirebaseAuth.getInstance().signOut(); //파이어베이스 로그아웃
                Toast.makeText(MainActivity.this.getApplicationContext(), "로그아웃이 되었습니다", Toast.LENGTH_SHORT).show();
                overridePendingTransition(android.R.anim.fade_in,android.R.anim.fade_out);
                finish();
                Intent intent = new Intent(MainActivity.this, User_Login.class);
                startActivity(intent);
            }
        });
    }


    public void result_check(){
        FirebaseFirestore db = FirebaseFirestore.getInstance();
        db.collection(user.getEmail()).get().addOnCompleteListener(new OnCompleteListener<QuerySnapshot>() {
            @Override
            public void onComplete(@NonNull Task<QuerySnapshot> task) {
                if(task.isSuccessful()){
                    for (QueryDocumentSnapshot document : task.getResult()){
                        String str = document.getData().toString();

                        String target5 = "result=";
                        int target_num5 = str.indexOf(target5);
                        String result= str.substring(target_num5,(str.substring(target_num5).indexOf(",")+target_num5));
                        String result2 = result.substring(result.indexOf("=")+1);




                        String target2 = "area=";
                        int target_num2 = str.indexOf(target2);
                        String area = str.substring(target_num2,(str.substring(target_num2).indexOf(",")+target_num2));
                        String area2 = area.substring(area.indexOf("=")+1);


                        String target3 = "round=";
                        int target_num3 = str.indexOf(target3);
                        String round = str.substring(target_num3,(str.substring(target_num3).indexOf(",")+target_num3));
                        String round2 = round.substring(round.indexOf("=")+1);

                        String value = area2+"/"+round2;

                        String target4 = "user=";
                        int target_num4 = str.indexOf(target4);
                        String user = str.substring(target_num4,(str.substring(target_num4).indexOf("}")+target_num4));
                        String user2 = user.substring(user.indexOf("=")+1);

                        String target = "time=";
                        int target_num = str.indexOf(target);
                        String time = str.substring(target_num,(str.substring(target_num).indexOf(",")+target_num));
                        String time2 = time.substring(time.indexOf("=")+1);



                        main_adapter.setArrayData(result2, value, user2, time2);
                        System.out.println(document.getData().toString());
                        recyclerView.setAdapter(main_adapter);
                    }
                }
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
    //플로팅메뉴 애니메이션
    public void anim() {

        if (isFabOpen) {
            fab1.startAnimation(fab_close);
            fab1.setClickable(false);
            isFabOpen = false;
        } else {
            fab1.startAnimation(fab_open);
            fab1.setClickable(true);
            isFabOpen = true;
        }
    }
}