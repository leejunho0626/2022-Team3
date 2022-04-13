package com.example.team3_project;

import android.content.Context;
import android.view.View;
import android.widget.TextView;

import androidx.recyclerview.widget.RecyclerView;


class ViewHolder extends RecyclerView.ViewHolder{
    TextView txt_result;

    ViewHolder(Context context, View itemView){
        super(itemView);
        txt_result = itemView.findViewById(R.id.txt_result);
    }

}
