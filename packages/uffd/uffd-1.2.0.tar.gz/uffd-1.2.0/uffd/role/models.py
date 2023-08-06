from sqlalchemy import Column, String, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import MappedCollection, collection
from sqlalchemy.ext.declarative import declared_attr

from uffd.ldapalchemy.dbutils import DBRelationship
from uffd.database import db
from uffd.user.models import User, Group

class RoleGroup(db.Model):
	__tablename__ = 'role-group'
	role_id = Column(Integer(), ForeignKey('role.id'), primary_key=True)
	group_dn = Column(String(128), primary_key=True)
	requires_mfa = Column(Boolean(), default=False, nullable=False)

	role = relationship('Role')
	group = DBRelationship('group_dn', Group)

class RoleUser(db.Model):
	__tablename__ = 'role-user'
	__table_args__ = (
		db.UniqueConstraint('dn', 'role_id'),
	)

	id = Column(Integer(), primary_key=True, autoincrement=True)
	dn = Column(String(128))

	@declared_attr
	def role_id(self):
		return Column(ForeignKey('role.id'))

# pylint: disable=E1101
role_inclusion = db.Table('role-inclusion',
	Column('role_id', Integer, ForeignKey('role.id'), primary_key=True),
	Column('included_role_id', Integer, ForeignKey('role.id'), primary_key=True)
)

def flatten_recursive(objs, attr):
	'''Returns a set of objects and all objects included in object.`attr` recursivly while avoiding loops'''
	objs = set(objs)
	new_objs = set(objs)
	while new_objs:
		for obj in getattr(new_objs.pop(), attr):
			if obj not in objs:
				objs.add(obj)
				new_objs.add(obj)
	return objs

def get_user_roles_effective(user):
	base = set(user.roles)
	if not user.is_service_user:
		base.update(Role.query.filter_by(is_default=True))
	return flatten_recursive(base, 'included_roles')

User.roles_effective = property(get_user_roles_effective)

def compute_user_groups(user, ignore_mfa=False):
	groups = set()
	for role in user.roles_effective:
		for group in role.groups:
			if ignore_mfa or not role.groups[group].requires_mfa or user.mfa_enabled:
				groups.add(group)
	return groups

User.compute_groups = compute_user_groups

def update_user_groups(user):
	current_groups = set(user.groups)
	groups = user.compute_groups()
	if groups == current_groups:
		return set(), set()
	groups_added = groups - current_groups
	groups_removed = current_groups - groups
	for group in groups_removed:
		user.groups.discard(group)
	user.groups.update(groups_added)
	return groups_added, groups_removed

User.update_groups = update_user_groups

class RoleGroupMap(MappedCollection):
	def __init__(self):
		super().__init__(keyfunc=lambda rolegroup: rolegroup.group)

	@collection.internally_instrumented
	def __setitem__(self, key, value, _sa_initiator=None):
		value.group = key
		super().__setitem__(key, value, _sa_initiator)

class Role(db.Model):
	__tablename__ = 'role'
	id = Column(Integer(), primary_key=True, autoincrement=True)
	name = Column(String(32), unique=True)
	description = Column(Text(), default='')
	included_roles = relationship('Role', secondary=role_inclusion,
	                               primaryjoin=id == role_inclusion.c.role_id,
	                               secondaryjoin=id == role_inclusion.c.included_role_id,
																 backref='including_roles')
	including_roles = [] # overwritten by backref

	moderator_group_dn = Column(String(128), nullable=True)
	moderator_group = DBRelationship('moderator_group_dn', Group)

	db_members = relationship("RoleUser", backref="role", cascade="all, delete-orphan")
	members = DBRelationship('db_members', User, RoleUser, backattr='role', backref='roles')

	groups = relationship('RoleGroup', collection_class=RoleGroupMap, cascade='all, delete-orphan')

	# Roles that are managed externally (e.g. by Ansible) can be locked to
	# prevent accidental editing of name, moderator group, included roles
	# and groups as well as deletion in the web interface.
	locked = Column(Boolean(), default=False, nullable=False)

	is_default = Column(Boolean(), default=False, nullable=False)

	@property
	def members_effective(self):
		members = set()
		for role in flatten_recursive([self], 'including_roles'):
			members.update(role.members)
			if role.is_default:
				members.update([user for user in User.query.all() if not user.is_service_user])
		return members

	@property
	def included_roles_recursive(self):
		return flatten_recursive(self.included_roles, 'included_roles')

	@property
	def groups_effective(self):
		groups = set(self.groups)
		for role in self.included_roles_recursive:
			groups.update(role.groups)
		return groups

	def update_member_groups(self):
		for user in self.members_effective:
			user.update_groups()
