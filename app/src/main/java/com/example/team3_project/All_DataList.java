package com.example.team3_project;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;
import androidx.core.app.ActivityCompat;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

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
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.QueryDocumentSnapshot;
import com.google.firebase.firestore.QuerySnapshot;

import java.util.ArrayList;

public class All_DataList extends AppCompatActivity {

    private static Animation fab_open, fab_close;
    private static Boolean isFabOpen = false;
    private static FloatingActionButton fab, fab1;
    FirebaseAuth firebaseAuth;
    FirebaseUser user = FirebaseAuth.getInstance().getCurrentUser();
    private long backPressedTime = 0;
    private final long FINISH_INTERVAL_TIME = 2000;
    TextView txt_aID;
    ArrayList<String> list = new ArrayList<>();
    RecyclerView recyclerView;
    All_Adapter all_adapter;

    //1. Firebase 실시간DB 객체 얻어오기
    FirebaseDatabase firebaseDatabase = FirebaseDatabase.getInstance();
    //2. 저장시킬 노드 참조객체 가져오기
    DatabaseReference ref = firebaseDatabase.getReference(); //()안에 내용이 없으면 최상위 노드

    SwipeRefreshLayout refresh_layout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.all_datalist);
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO); //다크모드 해제

        //플로팅 메뉴 설정
        fab_open = AnimationUtils.loadAnimation(All_DataList.this.getApplicationContext(), R.anim.fab_open);
        fab_close = AnimationUtils.loadAnimation(All_DataList.this.getApplicationContext(), R.anim.fab_close);
        fab = (FloatingActionButton) findViewById(R.id.a_fab);
        fab1 = (FloatingActionButton) findViewById(R.id.a_fab1);
        txt_aID = findViewById(R.id.txt_aID);
        firebaseAuth = FirebaseAuth.getInstance();
        all_adapter = new All_Adapter();
        recyclerView = findViewById(R.id.recyceler_allResult);
        recyclerView.setLayoutManager(new LinearLayoutManager(All_DataList.this, RecyclerView.VERTICAL, false));
        refresh_layout = findViewById(R.id.aRefresh_layout);

        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        String aID = bundle.getString("admin");

        txt_aID.setText(aID);
        aResult_check();

        refresh_layout.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh() {
                all_adapter.arrResult.clear();
                all_adapter.arrValue.clear();
                all_adapter.arrUser.clear();
                all_adapter.arrTime.clear();

                // 새로고침 코드를 작성
                aResult_check();
                all_adapter.notifyDataSetChanged();

                // 새로고침 완료시,
                // 새로고침 아이콘이 사라질 수 있게 isRefreshing = false
                refresh_layout.setRefreshing(false);
            }
        });

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
                Toast.makeText(All_DataList.this.getApplicationContext(), "로그아웃이 되었습니다", Toast.LENGTH_SHORT).show();
                overridePendingTransition(android.R.anim.fade_in,android.R.anim.fade_out);
                finish();
                Intent intent = new Intent(All_DataList.this, Login_Choice.class);
                startActivity(intent);
            }
        });
    }

    //검사 전체 결과 확인
    public void aResult_check(){
        FirebaseFirestore db = FirebaseFirestore.getInstance();
        db.collection("User").get().addOnCompleteListener(new OnCompleteListener<QuerySnapshot>() {
            @Override
            public void onComplete(@NonNull Task<QuerySnapshot> task) {
                if(task.isSuccessful()){
                    for (QueryDocumentSnapshot document : task.getResult()){
                        String str1 = document.getData().toString();

                        str1 = str1.substring((str1.indexOf("=")+1));
                        String result = str1.substring(0, str1.indexOf("}"));


                        db.collection(result).get().addOnCompleteListener(new OnCompleteListener<QuerySnapshot>() {
                            @Override
                            public void onComplete(@NonNull Task<QuerySnapshot> task) {
                                if(task.isSuccessful()){
                                    for(QueryDocumentSnapshot document : task.getResult()){
                                        String str = document.getData().toString();
                                        System.out.println("결과 : "+str);

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

                                        String value = round2+"/"+area2;

                                        String target4 = "user=";
                                        int target_num4 = str.indexOf(target4);
                                        String user = str.substring(target_num4,(str.substring(target_num4).indexOf("}")+target_num4));
                                        String user2 = user.substring(user.indexOf("=")+1);

                                        String target = "time=";
                                        int target_num = str.indexOf(target);
                                        String time = str.substring(target_num,(str.substring(target_num).indexOf(",")+target_num));
                                        String time2 = time.substring(time.indexOf("=")+1);



                                        all_adapter.setArrayData(result2, value, user2, time2);
                                        System.out.println(document.getData().toString());
                                        recyclerView.setAdapter(all_adapter);
                                    }
                                }

                            }
                        });
                        /*
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



                        all_adapter.setArrayData(result2, value, user2, time2);
                        System.out.println(document.getData().toString());
                        recyclerView.setAdapter(all_adapter);
                         */
                    }
                }
                else{
                    System.out.println("실패");
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