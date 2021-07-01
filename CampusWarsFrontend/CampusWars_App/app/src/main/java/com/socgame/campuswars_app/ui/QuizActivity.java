package com.socgame.campuswars_app.ui;

import android.content.Context;
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

public class QuizActivity extends AppCompatActivity implements View.OnClickListener
{
    /**
     * Gets Data from calling Activity via Bundle
     * creates Quiz Duel between 2 Players
     *
     * sends Data back to Server
     *
     * written by Jonas and Daniel
     */

    private Context ctx;
    private int gid;
    private int pid;
    private String oppName;
    private String oppTeam;
    private String question;
    private String[] wrongAnswers;
    private String correctAnswer;

    //TODO Link to Server

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_quiz);
        ctx = this.getApplicationContext();
        //Getting Data From Call
        Bundle b = getIntent().getExtras();
        //TODO Add topic Title, ADD challenger to Quiz Activity xml
        //TODO We get right answer now
        if(b != null){
            /*
            this.question = b.getString("question");
            this.answers = b.getStringArray("answers");
            this.correctAnswer = b.getInt("correctAnswer");
            this.challenger = b.getString("challenger");
            */
            //TODO FIXME FOR NEW HTTP CALL
            //MAYBE ADD CORRECT ANSWER TO ARRAY of WRONG ANSWERS AND THEN RANDOMIZE?
        }

        TextView textQuestion = (TextView) findViewById(R.id.questionText);
        TextView textTitle = (TextView) findViewById(R.id.topicText);

        Button option1 = (Button) findViewById(R.id.answerButtonA);
        Button option2 = (Button) findViewById(R.id.answerButtonB);
        Button option3 = (Button) findViewById(R.id.answerButtonC);
        Button option4 = (Button) findViewById(R.id.answerButtonD);

        textQuestion.setText(this.question);
        textTitle.setText(this.challenger); //TODO change this to topic Title and add Challenger textView

        option1.setText(this.answers[0]);
        option2.setText(this.answers[1]);
        option3.setText(this.answers[2]);
        option4.setText(this.answers[3]);

        option1.setOnClickListener(this);
        option2.setOnClickListener(this);
        option3.setOnClickListener(this);
        option4.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.answerButtonA:
                checkAnswer(1);
                break;
            case R.id.answerButtonB:
                checkAnswer(2);
                break;
            case R.id.answerButtonC:
                checkAnswer(3);
                break;
            case R.id.answerButtonD:
                checkAnswer(4);
                break;
            default:
                break;
        }
    }

    private void checkAnswer(int chosenAnswer){
        //TODO fix check
        /*
        if(chosenAnswer == this.correctAnswer){
            Toast.makeText(this.ctx, "Correct Answer, Congrats!", Toast.LENGTH_SHORT).show();
        } else{
            Toast.makeText(this.ctx, "Wrong Answer, Sad :(", Toast.LENGTH_SHORT).show();
        }*/
    }
}