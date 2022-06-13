package com.example.team3_project;

import android.content.Context;
import android.graphics.Color;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;


import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

public class All_Adapter extends RecyclerView.Adapter<ViewHolder> {
    ArrayList<String> arrTime;
    ArrayList<String> arrValue;
    ArrayList<String> arrResult;
    ArrayList<String> arrUser;

    public All_Adapter() {

        arrTime = new ArrayList<>();
        arrValue = new ArrayList<>();
        arrResult = new ArrayList<>();
        arrUser = new ArrayList<>();
    }
    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        Context context = parent.getContext();
        LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        View view = inflater.inflate(R.layout.item_result, parent, false);
        ViewHolder viewholder = new ViewHolder(context, view);
        return viewholder;
    }
    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) { //데이터 넣기

        String time = arrTime.get(position);
        String value= arrValue.get(position);
        String result = arrResult.get(position);
        String user = arrUser.get(position);

        if(result.equals("정상")){
            holder.txt_result.setTextColor(Color.BLUE);
            holder.txt_result.setText(position+1+". "+result);
        }

        holder.txt_result.setText(position+1+". "+result);
        holder.txt_value.setText(value);
        holder.txt_user.setText(user);
        holder.txt_time.setText(time);

    }
    @Override
    public int getItemViewType(int position) {
        return position;
    }
    @Override
    public int getItemCount() {
        return arrTime.size();
    }
    public void setArrayData(String result, String value, String user, String time) {

        arrResult.add(result);
        arrValue.add(value);
        arrUser.add(user);
        arrTime.add(time);

        notifyDataSetChanged();

    }
}
