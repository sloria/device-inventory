# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Adapter'
        db.create_table(u'devices_adapter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True)),
            ('responsible_party', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('make', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('purchased_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 12, 0, 0))),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 12, 0, 0))),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 12, 0, 0))),
            ('lendee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user.Lendee'], null=True, blank=True)),
            ('lender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('condition', self.gf('django.db.models.fields.CharField')(default='EX', max_length=2)),
            ('status', self.gf('django.db.models.fields.CharField')(default='CI', max_length=2)),
        ))
        db.send_create_signal(u'devices', ['Adapter'])

        # Adding model 'Case'
        db.create_table(u'devices_case', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True)),
            ('responsible_party', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('make', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('purchased_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 12, 0, 0))),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 12, 0, 0))),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 12, 0, 0))),
            ('lendee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user.Lendee'], null=True, blank=True)),
            ('lender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('condition', self.gf('django.db.models.fields.CharField')(default='EX', max_length=2)),
            ('status', self.gf('django.db.models.fields.CharField')(default='CI', max_length=2)),
        ))
        db.send_create_signal(u'devices', ['Case'])

        # Adding model 'Headphones'
        db.create_table(u'devices_headphones', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True)),
            ('responsible_party', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('make', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('purchased_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 12, 0, 0))),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 12, 0, 0))),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 12, 0, 0))),
            ('lendee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user.Lendee'], null=True, blank=True)),
            ('lender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('condition', self.gf('django.db.models.fields.CharField')(default='EX', max_length=2)),
            ('status', self.gf('django.db.models.fields.CharField')(default='CI', max_length=2)),
        ))
        db.send_create_signal(u'devices', ['Headphones'])


    def backwards(self, orm):
        # Deleting model 'Adapter'
        db.delete_table(u'devices_adapter')

        # Deleting model 'Case'
        db.delete_table(u'devices_case')

        # Deleting model 'Headphones'
        db.delete_table(u'devices_headphones')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'devices.adapter': {
            'Meta': {'ordering': "['-updated_at', '-created_at']", 'object_name': 'Adapter'},
            'condition': ('django.db.models.fields.CharField', [], {'default': "'EX'", 'max_length': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 12, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lendee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user.Lendee']", 'null': 'True', 'blank': 'True'}),
            'lender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'make': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'purchased_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 12, 0, 0)'}),
            'responsible_party': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'CI'", 'max_length': '2'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 12, 0, 0)'})
        },
        u'devices.case': {
            'Meta': {'ordering': "['-updated_at', '-created_at']", 'object_name': 'Case'},
            'condition': ('django.db.models.fields.CharField', [], {'default': "'EX'", 'max_length': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 12, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lendee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user.Lendee']", 'null': 'True', 'blank': 'True'}),
            'lender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'make': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'purchased_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 12, 0, 0)'}),
            'responsible_party': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'CI'", 'max_length': '2'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 12, 0, 0)'})
        },
        u'devices.comment': {
            'Meta': {'ordering': "['-updated_at', '-created_at']", 'object_name': 'Comment'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 12, 0, 0)'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['devices.Ipad']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 12, 0, 0)'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['auth.User']"})
        },
        u'devices.headphones': {
            'Meta': {'ordering': "['-updated_at', '-created_at']", 'object_name': 'Headphones'},
            'condition': ('django.db.models.fields.CharField', [], {'default': "'EX'", 'max_length': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 12, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lendee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user.Lendee']", 'null': 'True', 'blank': 'True'}),
            'lender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'make': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'purchased_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 12, 0, 0)'}),
            'responsible_party': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'CI'", 'max_length': '2'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 12, 0, 0)'})
        },
        u'devices.ipad': {
            'Meta': {'ordering': "['-updated_at', '-created_at']", 'object_name': 'Ipad'},
            'condition': ('django.db.models.fields.CharField', [], {'default': "'EX'", 'max_length': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 12, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lendee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user.Lendee']", 'null': 'True', 'blank': 'True'}),
            'lender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'make': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'purchased_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 12, 0, 0)'}),
            'responsible_party': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'IN'", 'max_length': '2'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 12, 0, 0)'})
        },
        u'user.lendee': {
            'Meta': {'object_name': 'Lendee'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['user.Subject']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'lendee_user'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'user.subject': {
            'Meta': {'object_name': 'Subject'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'subject_id': ('django.db.models.fields.IntegerField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['devices']