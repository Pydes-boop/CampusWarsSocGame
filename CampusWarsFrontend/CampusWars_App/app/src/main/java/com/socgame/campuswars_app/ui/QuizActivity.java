package com.socgame.campuswars_app.ui;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;

import com.google.android.material.snackbar.Snackbar;

import androidx.appcompat.app.AppCompatActivity;

import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import com.socgame.campuswars_app.R;
import com.socgame.campuswars_app.databinding.ActivityQuizBinding;

import org.w3c.dom.Text;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * Gets Data from calling Activity via Bundle
 * creates Quiz Duel between 2 Players
 *
 * sends Data back to Server
 *
 * written by Jonas and Daniel
 */
public class QuizActivity extends AppCompatActivity //implements View.OnClickListener
{
    private Context ctx;

    private int gameId;
    private int playerId; //0/1

    //cant display this yet
    private String oppName;
    private String oppTeam;

    private String question;
    private String[] wrongAnswers;//3 lang
    private String correctAnswer;

    private int indexRight = -1;

    //UI
    Button buttons[] = new Button[4];

    //TODO Link to Server

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_quiz);
        ctx = this.getApplicationContext();

        /*
        //TODO: get proper info from server
        //Getting Data From Call
        Bundle b = getIntent().getExtras();
        //TODO Add topic Title, ADD challenger to Quiz Activity xml
        //TODO We get right answer now
        if(b != null)
        {

            //this.question = b.getString("question");
            //this.answers = b.getStringArray("answers");
            //this.correctAnswer = b.getInt("correctAnswer");
            //this.challenger = b.getString("challenger");

            //TODO FIXME FOR NEW HTTP CALL
            //MAYBE ADD CORRECT ANSWER TO ARRAY of WRONG ANSWERS AND THEN RANDOMIZE?
        }
        */

        debugValues();

        setUI();
    }

    //TODO: this can be deleted once the http call is inplace
    private void debugValues()
    {
        gameId = 0;
        playerId = 0; //0/1

        //cant display this yet
        oppName = "test enemy";
        oppTeam = "evil team";

        question = "What is the average air speed velocity of a laden swallow?";
        String[] temp = {"40 m/s", "Faster than an ant, slower than a bee", "Wouldnt you like to know, weatherboy?"};
        wrongAnswers = temp;//3 lang
        correctAnswer = "What do you mean, an African or European Swallow?";
    }


    private void setUI()
    {
        //Set UI text

        //TODO: get topic text
        TextView topicText = this.findViewById(R.id.topicText);
        topicText.setText("TODO: get real topic");

        //Also what do I do with the opposing team/player name?


        //Randomize answer order
        List<String> allAnswers = Arrays.asList(wrongAnswers);
        allAnswers.add(correctAnswer);
        Collections.shuffle(allAnswers);
        indexRight = allAnswers.indexOf(correctAnswer);


        //give answers to buttons
        buttons[0] = this.findViewById(R.id.answerButtonA);
        buttons[1] = this.findViewById(R.id.answerButtonB);
        buttons[2] = this.findViewById(R.id.answerButtonC);
        buttons[3] = this.findViewById(R.id.answerButtonD);

        for(int i = 0; i < buttons.length; i++)
        {
            buttons[i].setText(allAnswers.get(i));
        }


        //set responses
        buttons[0].setOnClickListener(new View.OnClickListener()
        {
            public void onClick(View view){ answer(0);}
        });

        buttons[1].setOnClickListener(new View.OnClickListener()
        {
            public void onClick(View view){ answer(1);}
        });

        buttons[2].setOnClickListener(new View.OnClickListener()
        {
            public void onClick(View view){ answer(2);}
        });

        buttons[3].setOnClickListener(new View.OnClickListener()
        {
            public void onClick(View view){ answer(3);}
        });
    }

    private void answer(int buttonIndex)
    {
        //TODO: send answer to server

        if(buttonIndex == indexRight) //Correct Answer
        {
            Toast.makeText(this, "Correct!", Toast.LENGTH_LONG).show();
        }
        else //wrong answer
        {
            Toast.makeText(this, "False", Toast.LENGTH_LONG).show();
        }
    }
}