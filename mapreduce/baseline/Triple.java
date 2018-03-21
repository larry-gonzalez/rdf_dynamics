import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.io.ByteArrayInputStream;


import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.StmtIterator;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.rdf.model.Property;
import org.apache.jena.rdf.model.RDFNode;
import org.apache.jena.rdf.model.Statement;
import org.apache.jena.rdf.model.Literal;

import org.apache.hadoop.io.Writable;



public class Triple implements Writable {
    private String sub = ""; 
    private String pre = ""; 
    private String obj = ""; 
    private boolean literal = false; //true if object is literal, false if it is not

    public String getSub() { return this.sub; }
    public String getPre() { return this.pre; }
    public String getObj() { return this.obj; }
    public boolean literal() {return this.literal; }

    public void setSub(String sub) { this.sub = sub; }
    public void setPre(String pre) { this.pre = pre; }
    public void setObj(String obg) { this.obj = obj; }

    public void setLine(String line){
        Model model = ModelFactory.createDefaultModel();
        model.read(new ByteArrayInputStream(line.toString().getBytes()), null, "N-TRIPLES");

        StmtIterator iter = model.listStatements();
        Statement stmt = iter.nextStatement();

        this.sub = "<" + stmt.getSubject().toString() + ">";
        this.pre = "<" + stmt.getPredicate().toString() + ">";
        RDFNode res = stmt.getObject();
        if (res instanceof Resource) {
            this.obj =  "<" + res.toString() + ">";
            this.literal = true;
        } else {
            Literal li = (Literal) res;
            String la = li.getLanguage();
            this.obj =  "\"" + li.getString() + "\"";
            if (! la.equals("")) {
                this.obj += "@" + la; 
            }
        }
    }

    @Override
    public void readFields(DataInput in) throws IOException {
        sub = new String(in.readUTF());
        pre = new String(in.readUTF());
        obj = new String(in.readUTF());
        literal = in.readBoolean();
    }

    @Override
    public void write(DataOutput out) throws IOException {
        out.writeUTF(this.sub);
        out.writeUTF(this.pre);
        out.writeUTF(this.obj);
        out.writeBoolean(this.literal);
    }

    @Override
    public String toString() { return sub + "\t" + pre + "\t" + obj; }

}
