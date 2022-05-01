package com.example.team3_project;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckBox;
import android.widget.CompoundButton;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

import static android.content.ContentValues.TAG;

public class Main_Adapter extends RecyclerView.Adapter<ViewHolder> {
    ArrayList<String> arrTime;
    ArrayList<String> arrValue;
    ArrayList<String> arrResult;
    ArrayList<String> arrUser;

    public Main_Adapter() {

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
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {

        String time = arrTime.get(position);
        String value= arrValue.get(position);
        String result = arrResult.get(position);
        String user = arrUser.get(position);

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
